from text_handlers import *
from textblob import TextBlob,Word

slurs = set([
    'ching chong','chink','christ-killer','christ killer','gook',
    'goy','half-breed','half breed', 'heeb','hebe','kike','jewboy',
    'jigaboo','jiggabo', 'jig', 'jigga', 'jigger', 'jungle bunny',
    'kyke','niglet','nig-nog', 'nig nog', 'nignog','nigger',
    'nigga', 'nigress','niggah', 'nigga','porch monkey','raghead',
    'rag head', 'sambo','shylock','slant-eye', 'slant eye','spic',
    'spick','spik','tar baby','tar-baby','tyrone','towel head', 
    'uncle tom','wetback','beaner','camel jockey','coon-ass','coon',
    'tnb','yard ape','welfare queen', 'unemployus', 'satchmo','sambo',
    'race traitor','race-traitor','mammy','pickaninny','sheboon',
    'furfag','chimpout','fag','faggot','queer','dyke','cocksucker'
])
def slurred(comment):
    '''
    Takes in a comment and returns either 1 (if slur is present) or 0
    (if no slur is present).

    Parameters:
    -----------

    comment:    str:    string to parse for comments.

    Returns:
    --------

    int: [0,1]
    '''
    comment_words = set(clean_text(comment,False,False).split())
    return int(len(comment_words.intersection(slurs)) > 0)

def lemmatize(comment):
    '''
    Takes in a comment, cleans it up, splits it into individual words,
    then returns the lemmatized forms of each of those words
    
    Parameters:
    -----------
    comment:        str:    string to be lemmatized.

    Returns:
    --------
    return_string:  str:    lemmatized string
    '''
    return_string = ''

    for words in clean_text(comment,False,False).split():
        if not words:
            continue
        return_string += ' '
        return_string += Word(words).lemmatize()
