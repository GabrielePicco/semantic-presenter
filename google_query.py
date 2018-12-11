from bs4 import BeautifulSoup
import urllib
import urllib.request
import json

"""
Google module utility for doing query
"""


def get_image_url(query, limit):
    """Get an array of images relatives to the query keywords

    Parameters
    -----------
    query: a string that contain the keywords
    limit: limit number of images returned

    Returns
    --------
    urls_image: an array of image url
    """
    query = query.replace("&", "").split()
    query = '+'.join(query)
    url = "https://www.google.it/search?q="+query+"&source=lnms&tbm=isch"
    header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')
    tags = soup.find_all("div", {"class": "rg_meta"}, limit=limit)
    urls_image = [json.loads(a.text)["ou"] for a in tags]
    return urls_image


def get_video_url(query, limit):
    """Get an array of videos relatives to the query keywords

    Parameters
    -----------
    query: a string that contain the keywords
    limit: limit number of videos returned

    Returns
    --------
    urls_video: an array of videos url
    """
    query = query.replace("&", "").split()
    query = '+'.join(query)
    url = "https://www.youtube.com/results?search_query=" + query
    header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')
    tags = soup.find_all("button", {'class': 'addto-tv-queue-button'}, limit=limit)
    urls_video = ["https://www.youtube.com/embed/" + url.get('data-video-ids') for url in tags]
    return urls_video


def get_article(query, limit):
    """Get an array of articles (title,link) relatives to the query keywords

    Parameters
    -----------
    query: a string that contain the keywords
    limit: limit number of articles (title,link) returned

    Returns
    --------
    aticles: an array of articles (title,link) url
    """
    query = query.replace("&", "").split()
    query = '+'.join(query)
    url = "https://www.google.it/search?q=" + query
    header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')
    tags = soup.find_all("div", {'class': 'r'}, limit=limit)
    articles = [(url.find('h3').text, url.find('a').get('href')) for url in tags]
    return articles
