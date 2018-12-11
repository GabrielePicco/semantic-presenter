import urllib.parse
import urllib.request
import urllib
from bs4 import BeautifulSoup
from stop_words import get_stop_words

"""
Utility module for find keywords from text or url
"""


def get_word_more_frequent_from_url(url, limit=-1):
    """Get the words more frequent from an url

    Parameters
    -----------
    url: the url
    limit: limit number of words returned

    Returns
    --------
    word_list: list of the words more frequent
    """
    if "%" in url:
        url = urllib.parse.unquote(url)
    text = get_text_from_url(url)
    text = urllib.parse.quote(text.encode('ascii', 'ignore'))
    text = text.replace("%20", " ")
    word_list = get_word_list(text)
    return get_list_word_more_frequent(word_list, limit)


def get_word_more_frequent_from_text(text, limit=-1):
    """Get the words more frequent from a text

    Parameters
    -----------
    text: text to search keywords
    limit: limit number of words returned

    Returns
    --------
    word_list: list of the words more frequent
    """
    word_list = get_word_list(text)
    return get_list_word_more_frequent(word_list, limit)


def get_word_list(content):
    """Get the list of word in the content

    Parameters
    -----------
    content: text to search keywords

    Returns
    --------
    word_list: list of the words more frequent
    """
    word_list = []
    content = content.replace("+", " ")
    # lowercase and split into an array
    words = content.lower().split()

    # for each word
    for word in words:
        # remove non-chars
        cleaned_word = __clean_word(word)
        # if there is still something there
        if len(cleaned_word) > 0:
            # add it to our word list
            word_list.append(cleaned_word)

    word_list = __remove_stop_words(word_list, "it")
    word_list = __remove_stop_words(word_list, "en")

    return word_list


def get_list_word_more_frequent(word_list, limit=-1):
    """Get the list of words more frequent

    Parameters
    -----------
    word_list: list of words
    limit: limit number of words returned

    Returns
    --------
    word_list: list of the words more frequent
    """
    word_count = {}
    for word in word_list:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    word_count = sorted(word_count, key=word_count.__getitem__, reverse=True)
    if limit != -1:
        word_count = word_count[:limit]
    return word_count


def get_text_from_url(url):
    """Get text from all p of an url

    Parameters
    -----------
    url: the url

    Returns
    --------
    page: string that contain the text of the page
    """
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')
    page = ""
    for text in soup.findAll('p'):
        if text.text is not None:
            content = text.text
            page += " " + content
    return page


def __remove_stop_words(words, language):
    """Remove the stop words from a given language to words

    Parameters
    -----------
    words: list of words
    language: the language

    Returns
    --------
    word_list: list of words without stop words
    """
    stop_words = get_stop_words(language)

    temp_list = []
    for value in words:
        if urllib.parse.unquote(value) not in stop_words:
            temp_list.append(value)

    return temp_list


def __clean_word(word):
    """Remove the useless character from a word

    Parameters
    -----------
    word: the word

    Returns
    --------
    word: the cleaned word
    """
    word = urllib.parse.unquote(word)
    not_useful = [",", ".", "(", ")", "\\", "/", ":"]
    for nc in not_useful:
        word = word.replace(nc, "")
    return urllib.parse.quote(word)
