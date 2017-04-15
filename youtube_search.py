#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

def search(query):
    base_url = "https://www.youtube.com/"
    url = base_url + "results?search_query=" + query
    session = requests.session()
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    video_urls = []
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        video_urls.append(base_url + vid['href'])
    return video_urls

def main():
    video_urls = search("burning stars mimicking birds")
    print(video_urls)

if __name__ == "__main__":
    main()

