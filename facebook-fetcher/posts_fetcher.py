import facebook
import pika
import configparser
import json
import arrow
import pprint
from helper import facebook_helper as fb
from helper import log_helper
from helper import rabbitmq_helper as rabbit
from helper import mongo_helper as mongodb
from pymongo.errors import DuplicateKeyError

logger = log_helper.get_logger('facebook-posts-fetcher')

QUEUE_EXCHANGE = "fb:posts"
LOWER_POST_DATE = arrow.get('2017-08-31 17:00:00', 'YYYY-MM-DD HH:mm:ss')
UPPER_POST_DATE = arrow.get('2017-10-01 17:00:00', 'YYYY-MM-DD HH:mm:ss')

config = configparser.ConfigParser()
config.read('config/production.ini')

mongo_client = mongodb.get_mongo_client(config['mongodb']['uri'])
posts_collection = mongo_client.guess_what_facebook.posts

queue_channel = rabbit.get_rabbit_channel(
    user=config['rabbitmq']['user'],
    password=config['rabbitmq']['pass'],
    host=config['rabbitmq']['host'],
    port=int(config['rabbitmq']['port']),
)

# create exchange
queue_channel.exchange_declare(
    exchange=QUEUE_EXCHANGE,
    exchange_type='fanout'
)
# create queues
queue_channel.queue_declare(queue='fb:page:get-posts', durable=True)
queue_channel.queue_declare(queue='fb:post:get-reactions', durable=True)
queue_channel.queue_declare(queue='fb:post:get-comments', durable=True)
# bind queues to an exchange
queue_channel.queue_bind(
    exchange=QUEUE_EXCHANGE,
    queue="fb:post:get-reactions",
)
queue_channel.queue_bind(
    exchange=QUEUE_EXCHANGE,
    queue="fb:post:get-comments",
)

graph = fb.get_facebook_graph(access_token=config['facebook']['user_token'])

def callback(ch, method, properties, body):
    page = json.loads(body.decode('utf-8'))
    page_id = page["page_id"]

    feed = graph.get_object(
        id=page_id + "/feed",
        fields=fb.FIELDS_OF_POST,
        limit=fb.POSTS_LIMIT_PER_PAGE
    )

    page_count = 1
    fetch_next_page = True

    while fetch_next_page:
        logger.info('----------------- Page {} of page_id {}, posts length = {} -----------------'.format(
                page_count,
                page_id,
                len(feed['data'])
            ))
        for post in feed['data']:
            all_reactions = []
            post_id = post['id']
            post_created_time = arrow.get(post['created_time'])
            logger.info('----------------- {} -----------------'.format(post_id))
            if post_created_time < LOWER_POST_DATE or post_created_time > UPPER_POST_DATE: 
                logger.info('[-] Drop outbound post, post_id = {}, created_time = {}'.format(
                    post_id, 
                    post_created_time
                ))
            else:
                # insert post to db
                logger.info('[+] Insert post to DB, post_id = {}, created_time = {}'.format(
                    post_id, 
                    post_created_time
                ))
                post['_id'] = post['id']
                try:
                    post_id = posts_collection.insert_one(post).inserted_id 
                except DuplicateKeyError:
                    pass

                logger.info('[++] Send post to queue, post_id = {}, created_time = {}'.format(
                    post_id, 
                    post_created_time
                ))
                
                # send to queue
                queue_channel.basic_publish(
                    exchange=QUEUE_EXCHANGE,
                    routing_key='',
                    body=json.dumps(post),
                    properties=pika.BasicProperties(
                        delivery_mode = 2, # make message persistent
                    )
                )
                pass
        
        if (arrow.get(feed['data'][-1]['created_time']) > LOWER_POST_DATE):
            logger.info('Last created_time of this page is {}'.format(feed['data'][-1]['created_time']))
            logger.info('Get next page ...')
            feed = fb.get_next_page_of_feed(
                graph=graph, 
                page_id=page_id, 
                after=feed['paging']['cursors']['after']
            )
            fetch_next_page = True
        else:
            logger.info('*** Last post of this page is older than {}'.format(LOWER_POST_DATE))
            logger.info('*** OK, done')
            fetch_next_page = False

        print("")

queue_channel.basic_qos(prefetch_count=1)
queue_channel.basic_consume(
    callback,
    queue="fb:page:get-posts",
    no_ack=False)
queue_channel.start_consuming()
