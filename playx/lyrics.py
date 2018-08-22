#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
import sys
from .stringutils import (
    urlencode, remove_punct, compute_jaccard, remove_multiple_spaces
)


class ManualError(Exception):
    def __init__(self, args):
        self.args = args
    def display(self):
        print(' '.join(self.args))

def search_lyricswikia(query):
    print("Searching lyrics.wikia.com")
    query = remove_multiple_spaces(query).lower()
    tokens1 = query.split()
    query = urlencode(query.lower())
    url = "http://lyrics.wikia.com/wiki/Special:Search?query={}".format(query)
    response = urllib.request.urlopen(url)
    extractor = BeautifulSoup(response.read(), "html.parser")
    divs = extractor.find_all("li", {'class' : 'result'})
    matches = []
    for div in divs:
        anchor = div.findAll('a')[0]
        title = anchor.text
        title = remove_multiple_spaces(remove_punct(title)).lower()
        tokens2 = title.split()
        link = anchor.attrs['href']
        dist = compute_jaccard(tokens1, tokens2)
        matches.append((title, link, dist))
    matches = sorted(matches, key = lambda x : x[2], reverse=True)
    if not matches:
        return ""

    url_full = matches[0][1]
    response = urllib.request.urlopen(url_full)
    extractor = BeautifulSoup(response.read(), "html.parser")
    div = extractor.find('div', {'class' : 'lyricbox'})
    return "" if not div else div.get_text('\n').strip()

def search(url, query):
    """
        Searches the possible songs for this query.
        Returns the list of url for the song
    """

    # first encode
    query = urlencode(query.lower())
    url_query = "?q={}".format(query)
    url_search = url + url_query
    response = urllib.request.urlopen(url_search)
    extractor = BeautifulSoup(response.read(), "html.parser")
    anchors = []
    try:
        table = extractor.find_all("table", {'class' : 'table'})[0]
        rows = table.find_all('tr')
        anchors = [ row.find('td').find('a').get('href')  for row in rows ]

        # discard if the link/anchor is just a pagination link
        links = [ anchor for anchor in anchors if not url_query in anchor ]
        if len(links) < 1:
            raise ManualError("no songs...")
    except ManualError as merr:
        merr.display()
        link = []
    return links

def lyrics_full(url):
    response = urllib.request.urlopen(url)
    read_lyrics = response.read()
    soup = BeautifulSoup(read_lyrics, "html.parser")
    lyrics = soup.find_all("div", attrs={"class": None, "id": None})
    lyrics = [x.getText() for x in lyrics][0]
    return lyrics

def get_lyrics(query):
    url = "http://search.azlyrics.com/search.php"
    print("Searching...\nHave patience and be an awesome potato...")
    links = search(url, query)

    if links:
        lyrics = lyrics_full(links[0])
        return lyrics

def main():
    args =  sys.argv
    if(len(args) > 1):
        query = ' '.join(args[1::])
        lyric = search_lyricswikia(query)
        print(lyric)


if __name__ == "__main__":
    main()

