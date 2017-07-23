#!/usr/bin/env python3

"""
    A module related to youtube.

    Disclaimer :
        Following contents are injurious to your mind
        due to all those crawling shit
"""

from bs4 import BeautifulSoup
import requests
from stringutils import remove_multiple_spaces, replace_space, replace_character, escape_quotes

from utility import exe 

class YoutubeMetadata:
    SPACE = "#"
    """
        A data store to store the information of a youtube video
    """
    def __init__self(self):
        self.title = ""
        self.url = ""
        self.description = ""
        self.duration = ""
        self.hash = ""

    def get_hash(self):
        self.title = remove_multiple_spaces(self.title)
        self.hash = replace_space(self.title, self.SPACE)
        return self.hash

    def display(self):
        print("title : ", self.title)
        print("url : ", self.url)
        print("description : ", self.description)
        print("duration : ", self.duration)

    @staticmethod
    def reverse_hash(song_name):
        song_name = remove_multiple_spaces(song_name)
        return replace_character(song_name, YoutubeMetadata.SPACE, " ")

def get_youtube_streams(url):
    """
        Get both audio & vidoe stream urls for youtube
        using youtube-dl

        PS: I don't know how youtube-dl does the magic
    """
    print("Getting stream urls...")
    cli = "youtube-dl -g {}".format(url)
    output, error = exe(cli)
    stream_urls = output.split("\n")
    url = {}
    url['audio'] = stream_urls[1]
    url['video'] = stream_urls[0]
    print("Fetched stream urls...")
    return url

def search_youtube(query):
    """
        Behold the greatest magic trick ever : crawl and crawl...
    """
    print("Searching youtube for the song : {}\nHave patience...".format(query))
    base_url = "https://www.youtube.com"
    #url = base_url + "/results?search_query=" + query
    url = base_url + "//results?sp=EgIQAVAU&q=" + query
    session = requests.session()
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    """
    for vid in soup.find_all(attrs={'class':'yt-uix-tile-link'}):
        video_urls.append(base_url + vid['href'])
    """
    videos = []
    for tile in soup.find_all(attrs = {'class' : "yt-lockup-tile"}):
        yt_uix_tile = tile.find(attrs={'class' : 'yt-uix-tile-link'})
        youtube_metadata = YoutubeMetadata()
        youtube_metadata.url = base_url + yt_uix_tile['href']
        youtube_metadata.title = yt_uix_tile['title']
        description = tile.find("div", {'class' : 'yt-lockup-description'})
        youtube_metadata.description = description.get_text().strip() if description else "No description available"
        duration = tile.find("span", {'class' : 'video-time'})
        youtube_metadata.duration = duration.get_text() if duration else "uknown duration"
        videos.append(youtube_metadata)
    return videos

def main():
    url = "https://www.youtube.com/watch?v=-qfCrYwdqCA"
    urls = get_youtube_streams(url)
    print(urls)

if __name__ == "__main__":
    main()

