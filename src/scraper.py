#!/usr/bin/env python3
#%%
from sys import argv
from copy import deepcopy
import requests
import requests.auth
from json import load
from praw import Reddit
from textblob import TextBlob
from collections import deque
from pandas import DataFrame,Series,to_datetime,read_csv
#%%
def create_reddit_instance(authfile='/home/justin/.local/cache/reddit/info'):
    '''
    Creates a reddit instance.

    Parameters:
    -----------
    authfile:   str:    Path to file containing account information

    Returns:
    --------
    Reddit instance

    '''
    with open(authfile,'r') as credentials:
        creds = load(credentials)
    client_auth = requests.auth.HTTPBasicAuth(creds['ID'],creds['SECRET'])
    post_data = { 'grant_type':  'password',
                  'username':  creds['USER'],
                  'password':  creds['PASS']}
    headers = { 'User-Agent':creds['AGENT'] }
    response = requests.post('https://www.reddit.com/api/v1/access_token',
                             auth=client_auth,data=post_data,headers=headers)

    token = response.json()['access_token']
    headers = { "Authorization": token, 
                "User-Agent":    creds['AGENT']}
    response = requests.get("https://oauth.reddit.com/api/v1/me", 
                            headers=headers)

    return Reddit(client_id       = creds['ID'],
                  client_secret   = creds['SECRET'],
                  user_agent      = creds['AGENT'],
                  username        = creds['USER'],
                  password        = creds['PASS'])

searched_subs = ['AntiLGBTQIA','againsttrans','DiversityNews',
'hardunpopularopinon','thereareonly2genders','pics','justiceserved',
'metacanada']

not_conditions = ['jig is up','great ape','suspicious']

questionable = ['natsee','patter-recognition','pattern \
recognition']

slurs = ['ching chong','chink','christ-killer','christ killer',
'gook','goy','half-breed', 'half breed', 'heeb','hebe','kike',
'jewboy','jigaboo','jiggabo', 'jig', 'jigga','jigger',
'jungle bunny','kyke','niglet','nig-nog', 'nig nog','nignog',
'nigger','nigga', 'nigress','niggah', 'nigga','porch monkey',
'raghead','rag head', 'sambo','shylock','slant-eye',
'slant eye','spic','spick','spik','tar baby','tar-baby',
'tyrone','towel head', 'uncle tom','wetback','beaner',
'camel jockey','coon-ass','coon','539','1488','tnb',
'yard ape','welfare queen','unemployus','toucan sam',
'satchmo','sambo','race traitor','race-traitor','mammy',
'pickaninny','sheboon','furfag','chimpout']
#%%
existing_subreddit_scrapes= read_csv('data/problematic_325.csv')
comment_ids = set(existing_subreddit_scrapes['comment_id'].tolist())

def build_dataframe(comment, df, directory='/home/justin/.local/share/xdg/media/documents/textfiles/galvanize/slur-prediction/data',filename='comment_info'):
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
    df['reference_set'].add(comment.id)
    if not comment.author:
        df['author'].append('None')
    else:
        df['author'].append(comment.author.name)
    df['body'].append(comment.body)
    df['subreddit'].append(comment._submission.subreddit.display_name)
    df['sub_id'].append(comment._submission.id)
    df['url'].append(comment._submission.url)
    df['comment_id'].append(comment.id)
    df['comment_permalink'].append(comment.permalink)
    df['submission_permalink'].append(comment._submission.permalink)

    '''
    After any of the lists that are stored as dictionary values
    have grown by some integer multiple of 500, create a DataFrame
    from the dictionary and save it to a csv file.
    '''
    if len(df['author']) % 500 == 0:
        DataFrame(df).to_csv(f'{directory}/{filename}_vscode.csv')

def parse_comment_forest(CommentForest, df1,deq):
    '''
    Takes a CommentForest instance, adds the top-level comments
    to a dictionary where the comments and other possibly-useful
    information is stored, and adds the replies (another instance
    of CommentForest) to a queue for later processing

    Parameters:
    -----------

    CommentForest: Reddit CommentForest
    df1: dict
    deq: collections.deque
    '''
    CommentForest.replace_more(limit=None)
    author_len = len(df1['author'])
    for comment in CommentForest.list():
        if len(df1['author']) > author_len + 25:
            author_len = len(df1['author'])
            print(comment.body,end=' -|-+-|- ')
            print(author_len, ' -|-+-|- ', len(deq))
        if comment.id not in comment_ids:
            comment_ids.add(comment.id)
            build_dataframe(comment, df1, filename='problematic')
            deq.append(comment.replies)

info = {'author':[], 'url':[],'body':[],'subreddit':[],
        'sub_id':[],'comment_id':[],'comment_permalink':[],
        'submission_permalink':[],'reference_set':set()}
problematic,backup, backup_info = deepcopy(info),deepcopy(info),deepcopy(info)
queue = deque()
def scrape_subreddits(searched_subs, reddit, dictionary, queue):
    sorting_methods = \
        [ lambda sub: reddit.subreddit(sub).hot(),
          lambda sub: reddit.subreddit(sub).new(),
          lambda sub: reddit.subreddit(sub).top(),
          lambda sub: reddit.subreddit(sub).controversial() ]

    for subreddit in searched_subs:
        for sorting in sorting_methods:
            for submission in sorting(subreddit):
                parse_comment_forest(submission.comments,\
                                        dictionary,queue)
        while len(queue) >= 1:
            parse_comment_forest(queue.popleft(),\
                                dictionary, queue)
#%%
if __name__ =='__main__':
    pass