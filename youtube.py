#!/usr/bin/env python3

"""A module related to youtube.

Disclaimer : Following contents are injurious to your mind
due to all those crawling shit
"""

from bs4 import BeautifulSoup
import requests
from stringutils import remove_multiple_spaces, replace_space, replace_character
from cache import Cache

from utility import exe


class YoutubeMetadata:
    """A data store to store the information of a youtube video."""

    def __init__self(self):
        self.title = ""
        self.url = ""
        self.duration = ""

    def display(self):
        """Be informative."""
        print("Title: ", self.title)
        print("Duration: ", self.duration)

def get_youtube_streams(url):
    """Get both audio & vidoe stream urls for youtube using youtube-dl.

    PS: I don't know how youtube-dl does the magic
    """
    cli = "youtube-dl -g {}".format(url)
    output, error = exe(cli)
    stream_urls = output.split("\n")
    url = {}
    try:
        url['audio'] = stream_urls[1]
    except IndexError:
        url['audio'] = None
    url['video'] = stream_urls[0]
    return url

def get_youtube_title(url):
    print("Getting title for :: {}".format(url))
    cli = "youtube-dl -e {}".format(url)
    output, error = exe(cli)
    return output

def search_youtube(query):
    """Behold the greatest magic trick ever : crawl and crawl."""
    print("Searching youtube for :: {}".format(query))
    base_url = "https://www.youtube.com"
    url = base_url + "//results?sp=EgIQAVAU&q=" + query
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    """
    for vid in soup.find_all(attrs={'class':'yt-uix-tile-link'}):
        video_urls.append(base_url + vid['href'])
    """
    videos = []
    for tile in soup.find_all(attrs={'class': "yt-lockup-tile"}):
        yt_uix_tile = tile.find(attrs={'class': 'yt-uix-tile-link'})
        youtube_metadata = YoutubeMetadata()
        youtube_metadata.url = base_url + yt_uix_tile['href']
        youtube_metadata.title = yt_uix_tile['title']
        description = tile.find("div", {'class': 'yt-lockup-description'})
        youtube_metadata.description = description.get_text().strip() if description else "No description available"
        duration = tile.find("span", {'class': 'video-time'})
        youtube_metadata.duration = duration.get_text() if duration else "uknown duration"
        videos.append(youtube_metadata)
    return videos


def grab_link(value, title, no_cache):
    """Return the audio link of the song."""
    stream = get_youtube_streams(value)
    # Start downloading
    title = title + '.mp3'
    if stream['audio'] is None: return None
    value = stream['audio']
    if not no_cache:
        Cache.dw(value, title)
    return value


def main():
    """Run on program call."""
    url = "https://www.youtube.com/watch?v=erywPdFfORE"
    title = get_youtube_title(url)
    urls = get_youtube_streams(url)


if __name__ == "__main__":
    main()
