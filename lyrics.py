#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
import sys
from stringutils import urlencode


class ManualError(Exception):
    def __init__(self, args):
        self.args = args
    def display(self):
        print(' '.join(self.args))

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

def main():
    args =  sys.argv
    url = "http://search.azlyrics.com/search.php"
    links = []
    query = ""

    if(len(args) > 1):
        query = ' '.join(args[1::])
        print("Searching...\nHave patience and be an awesome potato...")
        links = search(url, query)

    if links:
        lyrics = lyrics_full(links[0])
        print(lyrics)

if __name__ == "__main__":
    main()

