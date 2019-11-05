from praw import Reddit
import requests
import requests.auth
from json import load
from pandas import DataFrame, read_csv, to_datetime, Series
from copy import deepcopy
from time import sleep
from collections import deque

creds = {}
with open('/home/justin/.local/cache/reddit/info','r') as credentials:
    creds = load(credentials)
client_auth = requests.auth.HTTPBasicAuth(creds['ID'],creds['SECRET'])
post_data = {'grant_type':'password','username':creds['USER'],'password':creds['PASS']}
headers = {'User-Agent':creds['AGENT']}
response = requests.post('https://www.reddit.com/api/v1/access_token',auth=client_auth,data=post_data,headers=headers)
token = response.json()['access_token']

reddit = Reddit(client_id=creds['ID'],
                client_secret=creds['SECRET'],
                user_agent=creds['AGENT'],
                username=creds['USER'],
                password=creds['PASS'])
project_dir = '/home/justin/.local/share/xdg/media/documents/textfiles/galvanize/slur-prediction/data'
file_contents='generic_scrapes'
queue = deque()
user_info = {'author':[], 'url':[],'body':[],'subreddit':[],
             'sub_id':[],'comment_id':[],'comment_permalink':[],
             'submission_permalink':[]}
searched_subs = ['pics','justiceserved']

def build_dataframe(comment, df, directory=project_dir, filename=file_contents):
    '''
    Takes Reddit Comment object and puts relevent attributes 
    into a dictionary that will be used to create a DataFrame.  
    The DataFrame will then be used to create a csv file for
    storage.
    
    Parameters:
    -----------
    
    comment: Reddit Comment instance
    df: dict
    directory: str
    filename: str
    
    Returns:
    --------
    
    None
    '''
    #df['reference_set'].add(comment.id)
    if not comment.author:
        df['author'].append('None')
    else:
        df['author'].append(comment.author.name)
    df['body'].append(comment.body)
    df['subreddit'].append(comment.subreddit.display_name)
    df['sub_id'].append(comment.submission.id)
    df['url'].append(comment.submission.url)
    df['comment_id'].append(comment.id)
    df['comment_permalink'].append(comment.permalink)
    df['submission_permalink'].append(comment._submission.permalink)
    
    '''
    After any of the lists that are stored as dictionary values
    have grown by some integer multiple of 500, create a DataFrame
    from the dictionary and save it to a csv file.
    '''
    if len(df['author']) % 500 == 0:
        DataFrame(df).to_csv(f'{directory}/{filename}_user_new.csv')

#def parse_comment_forest(CommentForest, df1,deq):
#    '''
#    Takes a CommentForest instance, adds the top-level comments
#    to a dictionary where the comments and other possibly-useful
#    information is stored, and adds the replies (another instance
#    of CommentForest) to a queue for later processing
#    
#    Parameters:
#    -----------
#    
#    CommentForest: Reddit CommentForest
#    df1: dict
#    deq: collections.deque
#    '''
#    CommentForest.replace_more(limit=None)
#    author_len = len(df1['author'])
#    for comment in CommentForest.list():
#        if len(df1['author']) > author_len + 25:
#            author_len = len(df1['author'])
#            print(comment.body,end=' -|-+-|- ')
#            print(author_len, ' -|-+-|- ', len(deq))
#        if comment.id not in comment_ids:
#            comment_ids.add(comment.id)
#            build_dataframe(comment, df1, filename='problematic_users')
#            deq.append(comment.replies)

def scrape(user, reddit, dictionary, queue):

    def get_controversial(user):
        return reddit.redditor(user).comments.controversial(limit=None)
    def get_hot(user):
        return reddit.redditor(user).comments.hot(limit=None)
    def get_new(user):
        return reddit.redditor(user).comments.new(limit=None)
    def get_top(user):
        return reddit.redditor(user).comments.controversial(limit=None)
    sorting_methods = \
    [
        lambda sub: reddit.redditor(user).comments.controversial(limit=None),
        lambda sub: reddit.redditor(user).comments.top(limit=None),
        lambda sub: reddit.redditor(user).comments.new(limit=None),
        lambda sub: reddit.redditor(user).comments.hot(limit=None)
    ]
    # for user in list(reddit_data['author'].unique()):

    for z in sorting_methods:
        for comment in z(user):
            if comment.id not in dictionary['comment_id']:
                build_dataframe(comment,dictionary)
                #parse_comment_forest(comment.replies, dictionary, queue)

def scrape_subreddits(searched_subs, reddit, dictionary, queue):
    sorting_methods = \
        [ lambda sub: reddit.subreddit(sub).hot(),
          lambda sub: reddit.subreddit(sub).new(),
          lambda sub: reddit.subreddit(sub).top(),
          lambda sub: reddit.subreddit(sub).controversial() ]

    for subreddit in searched_subs:
        for sorting in sorting_methods:
            for submission in sorting(subreddit):
                submission.comments.replace_more(limit=None)
                for comment in submission.comments.list():
                    print('starting with new redditor')
                    print(comment.author.name)
                    scrape(comment.author.name, reddit, dictionary,queue)
        #while len(queue) >= 1:
         #   parse_comment_forest(queue.popleft(),\
          #                      dictionary, queue)

if __name__ == '__main__':
    scrape_subreddits(searched_subs, reddit, user_info, queue)
    
        
