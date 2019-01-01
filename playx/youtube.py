#!/usr/bin/env python3

"""A module related to youtube.

Disclaimer : Following contents are injurious to your mind
due to all those crawling shit
"""

from bs4 import BeautifulSoup
import requests
from playx.stringutils import (
    remove_multiple_spaces,
    remove_punct
)

from playx.cache import Cache

from playx.utility import exe

from playx.logger import get_logger


# Setup logger
logger = get_logger('youtube')


class YoutubeMetadata:
    """A data store to store the information of a youtube video."""

    def __init__self(self):
        self.title = ""
        self.url = ""
        self.duration = ""

    def display(self):
        """Be informative."""
        logger.info("Title: {}".format(self.title))
        logger.info("Duration: {}".format(self.duration))

def get_youtube_streams(url):
    """Get both audio & video stream urls for youtube using youtube-dl.

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
    logger.info("Getting title for :: {}".format(url))
    cli = "youtube-dl -e {}".format(url)
    output, error = exe(cli)
    return output


def search_youtube(query):
    """Behold the greatest magic trick ever : crawl and crawl."""
    logger.info("Searching youtube for :: {}".format(query))
    base_url = "https://www.youtube.com"
    url = base_url + "//results?sp=EgIQAVAU&q=" + query
    try:
        response = requests.get(url)
    except Exception as e:
        logger.error("ERROR: ", e)
        exit()
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
        youtube_metadata.duration = duration.get_text() if duration else "unknown duration"
        videos.append(youtube_metadata)
    return videos


def grab_link(value):
    """Return the audio link of the song."""
    stream = get_youtube_streams(value)
    if stream['audio'] is None: return None
    value = stream['audio']
    # if not no_cache:
    #    Cache.dw(value, title)
    return value


def dw(title, url):
    # Start downloading
    title = remove_punct(title)
    title = remove_multiple_spaces(title)
    title = title + '.mp3'
    Cache.dw(url, title)

def main():
    """Run on program call."""
    url = "https://www.youtube.com/watch?v=erywPdFfORE"
    title = get_youtube_title(url)
    urls = get_youtube_streams(url)


if __name__ == "__main__":
    # main()
    search_youtube("Pehla nasha once again")
