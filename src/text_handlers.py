#%%
import string
import emoji
from unicodedata import name
from collections import defaultdict
from textblob import TextBlob
from collections import Counter
from pandas import Series

#%%
def remove_emoji(comment, replace_with_text=False):
    '''
    Helper function to remove emoji from a string.

    Parameters:
    -----------
    comment:            str:    String to be cleaned
    replace_with_text:  bool:   Whether or not the emoji will be 
                                    replaced or removed
    Returns:
    --------
    str:    cleaned string
    '''
    if replace_with_text:
        return replace_emoji(comment)
    else:
        return comment.encode('ascii','ignore').decode('ascii')

def count_words(comment):
    '''
    Helper function to count the number of words in a string.

    Parameters:
    -----------
    comment:       str: String whose words will be counted

    Returns:
    --------
    int:    number of words in string
    '''
    return len(comment.split())

def get_grams(comment,n=2,keep_emoji_words=False):
    '''
    Returns n-grams for a sentence, optionally cleaning the string
    in the process.

    Parameters:
    -----------
    comment:            str:    sentence for which n-grams will be 
                                    made
    n:                  int:    number of tokens to include in n-gram
    keep_emoji_words:   bool:   whether emoji will be removed or 
                                    substituted with text 
                                    descriptions
    Returns:
    --------
    list:   list of n-grams
    '''
    blob = TextBlob(clean_text(comment, keep_emoji_words=\
                                        keep_emoji_words))
    return list([' '.join(wordlist) for wordlist in blob.ngrams(n)])
# %%
def clean_text(comment, keep_periods=True,\
                        keep_emoji_words=False):
    '''
    Removes all punctuation (and, optionally, emoji/non-ascii 
    characters) from a string.

    Parameters:
    -----------
    comment:            str:    the string whose punctuation/emoji 
                                    will be removed
    keep_periods:       bool:   whether or not periods will also be 
                                    removed
    keep_emoji_words:   bool:   whether emoji will be removed or 
                                    replaced with string descriptions
    
    Returns:
    --------
    str:    cleaned text
    '''
    translation_dic = {key:None for key in string.punctuation}
    if keep_periods:
        del translation_dic['.']
        tr_tab = str.maketrans(translation_dic)
    else:
        tr_tab = str.maketrans(translation_dic)
    return remove_emoji(comment,keep_emoji_words).translate(tr_tab)

def count_emoji(comment):
    '''
    Function that counts number of emoji in a string.

    Parameters:
    -----------
    comment:    str:    String from which number of emoji will be 
                            counted and returned
    Returns:
    --------
    int:    number of emoji present in string
    '''
    return sum([
        1 for character in comment 
            if character in emoji.UNICODE_EMOJI.keys()
    ])
def replace_emoji(comment):
    '''
    Function to replace emoji in a string.

    Parameters:
    -----------
    comment:    str:    String from which emoji will be replaced

    Returns:
    --------
    str:    Cleaned string where emoji have been repalced with ascii
                characters describing the image
    '''
    return ''.join([
        '_'.join(name(character).split())+' ' if character in
        emoji.UNICODE_EMOJI else character for character
        in comment
    ])

def stopwords_list(series,fraction = 0.2):
    '''
    Takes in a pandas.core.Series object, iterates over it, creating
    a list of words, then finds the most frequently used words in the
    corpus.
    
    Parameters:
    -----------
    series:     pd.core.Series: Series whose words will be counted
    fraction:   float: fraction of words to throw out

    Returns:
    list:   list of (fraction) most-frequently used words
    '''
    out = []
    for elements in series:
        cleaned = clean_text(elements,False,False)
        num_words = count_words(cleaned)
        if num_words > 1:
            out.extend(cleaned.split())
        elif num_words == 1:
            out.append(cleaned)
    ctr = [(word,count) for word,count in Counter(out).items()]
    ctr.sort(key=lambda x:x[1])
    ctr = ctr[::-1]
    cutoff_index = int(fraction*len(ctr))
    stopwords = [word for word,number in ctr]
    return stopwords[:cutoff_index]

def series_grams(series,n=2):
    '''
    Function that returns a pandas.core.Series containing n-grams for
    each row in the series that is passed to it.

    Parameters:
    -----------
    series: pd.core.series.Series: Series containing comments out of 
                                which n-grams are to be made
    n:      int:            integer number of tokens to includ in 
                                each n-gram
    
    Returns:
    --------
    pd.core.series.Series
    '''
    out = []
    for elements in series:
        out.append(get_grams(elements.lower(),n))
    return Series(out)


# %%
def all_ngrams(series):
    '''
    Takes pandas.core.Series as argument, iterates over it, and 
    returns a set of all n-grams present in the series.

    Parameters:
    -----------
    series: pd.core.series.Series: series containing lists of ngrams

    Returns:
    --------
    out:    set:            set of all n-grams present in series
    '''

    out = set()
    for elements in series:
        for grams in elements:
            out.add(grams)
    return out

def make_dummies(df, col_name):
    '''
    Makes dummy columns from df column containing list of n-grams.

    Parameters:
    -----------
    df:         pd.core.frame.DataFrame:
    col_name:   str:    name of column from which dummies will be made

    Returns:
    pandas.core.frame.DataFrame
    '''

    gram_set = all_ngrams(df[col_name])
    for grams in gram_set:
        df[grams] = Series([0]*df.shape[0])
    for idx, row in df.iterrows():
        for grms in row[col_name]:
            df.loc[idx,grms] = 1
    del df[col_name]
    return df