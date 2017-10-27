import facebook
import log_helper

fb_logger = log_helper.get_logger('facebook-helper')

'''
https://graph.facebook.com/v2.10/204234332938286_1891024787592557/reactions?access_token=EAACEdEose0cBAP2nMN2FN66hk3aQVHzQNVGt277rkcsvAArdDwASuwUCDXzfDGSxzSxHddaT2VXX7gnNonAn0HtJlbfYTVIgAlXODZA8sNfVz51VIoH9LSmlEhiutorbtndjYsjl3O0yZC6AtqvK30m1yWFhdPZAmlwsyDeAAFGN81SZCcoEMqWT35I6iDsZD
&pretty=0
&limit=25
&after=TVRBd01ERTRPRE0yTmpjeE5EWXlPakUxTURrd056SXlNRFk2TWpVME1EazJNVFl4TXc9PQZDZD
'''


REACTION_LIMIT_PER_PAGE = 5000
LOWER_POST_DATE = arrow.get('2017-08-31 17:00:00', 'YYYY-MM-DD HH:mm:ss')
UPPER_POST_DATE = arrow.get('2017-10-01 17:00:00', 'YYYY-MM-DD HH:mm:ss')

def get_facebook_graph(access_token):
 return facebook.GraphAPI(access_token=access_token, version="2.7")

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
