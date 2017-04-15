#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

class YoutubeMetadata:
    def __init__self(self):
        self.title = ""
        self.url = ""
        self.description = ""
        self.duration = ""

    def display(self):
        print("title : ", self.title)
        print("url : ", self.url)
        print("description : ", self.description)
        print("duration : ", self.duration)

def search(query):
    base_url = "https://www.youtube.com/"
    url = base_url + "results?search_query=" + query
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
    videos = search("burning stars mimicking birds")
    for video in videos:
        video.display()

if __name__ == "__main__":
    main()

