import facebook
import arrow
from . import log_helper

fb_logger = log_helper.get_logger('facebook-helper')

'''
https://graph.facebook.com/v2.10/204234332938286_1891024787592557/reactions?access_token=EAACEdEose0cBAP2nMN2FN66hk3aQVHzQNVGt277rkcsvAArdDwASuwUCDXzfDGSxzSxHddaT2VXX7gnNonAn0HtJlbfYTVIgAlXODZA8sNfVz51VIoH9LSmlEhiutorbtndjYsjl3O0yZC6AtqvK30m1yWFhdPZAmlwsyDeAAFGN81SZCcoEMqWT35I6iDsZD
&pretty=0
&limit=25
&after=TVRBd01ERTRPRE0yTmpjeE5EWXlPakUxTURrd056SXlNRFk2TWpVME1EazJNVFl4TXc9PQZDZD
'''

POSTS_LIMIT_PER_PAGE = 100
COMMENTS_LIMIT_PER_PAGE=1000
REACTION_LIMIT_PER_PAGE = 5000
FIELDS_OF_POST="name,id,created_time,updated_time,message,message_tags,reactions"

def get_facebook_graph(access_token):
 return facebook.GraphAPI(access_token=access_token, version="2.7")

def get_next_page_of_feed(graph, page_id, after):
    response = graph.get_object(
        id=page_id + "/feed",
        fields=FIELDS_OF_POST,
        limit=POSTS_LIMIT_PER_PAGE,
        after=after,
    )
    return response

def get_reactions(graph, post_id, after):
    response = graph.get_object(
        id=post_id + '/reactions',
        after=after,
        limit=REACTION_LIMIT_PER_PAGE
    )
    return response

def get_all_reactions(graph, post_id, after):
    all_reactions = []
    response = get_reactions(post_id, after)
    fb_logger.debug('Reactions of post_id {}, reactions length = {}'.format(
        post_id, 
        len(response['data']))
    )
    while len(response['data']) > 0 and len(response['data']) > REACTION_LIMIT_PER_PAGE:
        fb_logger.debug('    Get next after {}'.format(response['paging']['cursors']['after']))
        all_reactions = all_reactions + response['data']
        response = get_reactions(
            graph=graph,
            post_id=post_id, 
            after=response['paging']['cursors']['after']
        )
        fb_logger.debug('    Length = '.format(len(response['data'])))
    return all_reactions

def get_comments(graph, post_id):
    fields = 'id,message,created_time,message_tags,application,from,parent,comments.summary(true).limit(0)';
    fields = fields + ',reactions.type(NONE).summary(total_count).limit(0).as(reactions_all)'
    fields = fields + ',reactions.type(LIKE).summary(total_count).limit(0).as(like)'
    fields = fields + ',reactions.type(LOVE).summary(total_count).limit(0).as(love)'
    fields = fields + ',reactions.type(WOW).summary(total_count).limit(0).as(wow)'
    fields = fields + ',reactions.type(HAHA).summary(total_count).limit(0).as(haha)'
    fields = fields + ',reactions.type(SAD).summary(total_count).limit(0).as(sad)'
    fields = fields + ',reactions.type(ANGRY).summary(total_count).limit(0).as(angry)'
    fields = fields + ',permalink_url,attachment&filter=stream&order=reverse_chronological'
    comments = []
    response = graph.get_object(
        id=post_id + '/reactions',
        fields=fields,
        after=after,
        limit=COMMENTS_LIMIT_PER_PAGE
    )
    comments = response['data']
    fb_logger.debug('Comments of post_id {}, comments length = {}'.format(
        post_id, 
        len(response['data']))
    )
    while len(response['data']) >= COMMENTS_LIMIT_PER_PAGE:
        fb_logger.debug('    Get next after {}'.format(response['paging']['cursors']['after']))
        after = response['paging']['cursors']['after']
        response = graph.get_object(
            id=post_id + '/reactions',
            fields=fields,
            after=after,
            limit=COMMENTS_LIMIT_PER_PAGE
        )
        fb_logger.debug('    Length = '.format(len(response['data'])))
        comments = comments + response['data']
    return response
