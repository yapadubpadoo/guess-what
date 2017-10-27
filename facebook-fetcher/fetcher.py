import facebook
import configparser
import arrow
import pprint
from facebook_helper import *
from helper import log_helper

logger = log_helper.get_logger('facebook-fetcher')

# app_id = config['facebook']['app_id']
# app_secret = config['facebook']['app_secret']
# app_token = config['facebook']['app_token']
access_token = config['facebook']['user_token']


graph = get_facebook_graph(access_token=access_token)
feed_ids = ['204234332938286/feed']

feed = graph.get_object(
    id="204234332938286/feed",
    fields="name,id,created_time,updated_time,message,message_tags,reactions",
    limit=100
)

for post in feed['data']:
    all_reactions = []
    post_id = post['id']
    post_created_time = arrow.get(post['created_time'])
    logger.info('----------------- {} -----------------'.format(post_id))
    if post_created_time < LOWER_POST_DATE or post_created_time > UPPER_POST_DATE: 
        logger.info('[-] Drop old post, post_id = {}, created_time = {}'.format(
            post_id, 
            post_created_time
        ))
    else:
        logger.info('[+] Send post to queue, post_id = {}, created_time = {}'.format(
            post_id, 
            post_created_time
        ))
        # logger.info('Getting reactions of post_id = {}, created_time {}'.format(
        #     post_id,
        #     post_created_time
        #     ))
        # if len(post['reactions']['data']) > 0:
        #     all_reactions = get_all_reactions(
        #         post_id=post_id, 
        #         after=post['reactions']['paging']['cursors']['after']
        #     )
        pass
    