#!/usr/bin/env python3

"""A module related to youtube.

Disclaimer : Following contents are injurious to your mind
due to all those crawling shit
"""

from bs4 import BeautifulSoup
import requests
from playx.stringutils import (
    fix_title,
    is_song_url
)

import re

from playx.cache import Cache

from playx.utility import exe

from playx.logger import Logger


# Setup logger
logger = Logger('youtube')

better_search_kw = [
                    ' audio',
                    ' full',
                    ' lyrics'
                  ]


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
    logger.debug("Extracting streamable links")
    logger.debug("{}".format(url))
    cli = "youtube-dl -g {}".format(url)
    output, error = exe(cli)
    logger.debug("{}".format(type(error)))

    if error != '':
        logger.critical("'{}' Error passed by youtube-dl. Please check if the latest version of youtube-dl is installed. You can report the error on https://yt-dl.org/bug.".format(error))

    logger.debug("O/P: {}".format(output))
    logger.debug("ERROR: {}".format(error))

    stream_urls = output.split("\n")
    url = {}
    try:
        url['audio'] = stream_urls[1]
    except IndexError:
        url['audio'] = None
    url['video'] = stream_urls[0]
    return url


def get_youtube_title(url):
    """
    Extract title of video from url.
    """
    logger.debug("Extracting title of passed URL")
    try:
        r = requests.get(url)
    except Exception as e:
        logger.error('ERROR: {}'.format(e))
        exit(-1)
    title = re.findall(r'<title>.*?</title>', r.text)[0]
    title = re.sub(r'title|>|<|/|\ ?-|\ ?YouTube', '', str(title))
    return title


def add_better_search_kw(query):
    """
    Add some keywords to the search querry to get better results.
    """
    if not is_song_url(query):
        for kw in better_search_kw:
            query += kw

    return query


def search_youtube(query, disable_kw=False):
    """Behold the greatest magic trick ever : crawl and crawl."""
    if not disable_kw:
        query = add_better_search_kw(query)
    logger.debug("Searching youtube for :: {}".format(query))
    base_url = "https://www.youtube.com"
    url = base_url + "//results?sp=EgIQAVAU&q=" + query
    try:
        response = requests.get(url)
    except Exception as e:
        logger.error("ERROR: ", e)
        exit()
    soup = BeautifulSoup(response.content, "html.parser")

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
    logger.debug(stream)
    if stream['audio'] is None: return None
    value = stream['audio']
    # if not no_cache:
    #    Cache.dw(value, title)
    return value


def dw(title, url):
    # Start downloading
    title = fix_title(title)
    Cache.dw(url, title)


def main():
    """Run on program call."""
    url = "https://www.youtube.com/watch?v=erywPdFfORE"
    title = get_youtube_title(url)
    urls = get_youtube_streams(url)


if __name__ == "__main__":
    # main()
    search_youtube("Pehla nasha once again")
