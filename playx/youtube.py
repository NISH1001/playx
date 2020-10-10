#!/usr/bin/env python3

"""A module related to youtube.

Disclaimer : Following contents are injurious to your mind
due to all those crawling shit
"""

import re
import sys

from bs4 import BeautifulSoup
from dataclasses import dataclass

import requests
import youtube_dl
from youtube_search import YoutubeSearch
from playx.stringutils import fix_title, is_song_url


from playx.cache import Cache

from playx.utility import exe

from playx.logger import Logger


# Setup logger
logger = Logger("youtube")

better_search_kw = [" audio", " full", " lyrics"]


@dataclass
class YoutubeMetadata:
    """A data store to store the information of a youtube video."""

    title: str = ""
    url: str = ""
    duration: str = ""

    def display(self):
        """Be informative."""
        logger.info(str(self))


def get_audio_URL(link):
    """Return true if the song is downloaded else false."""
    ydl_opts = {}
    ydl_opts["quiet"] = True
    ydl_opts["nocheckcertificate"] = True

    ydl = youtube_dl.YoutubeDL(ydl_opts)
    info = ydl.extract_info(link, download=False)
    try:
        audio_url = info["formats"][1]["url"]
        return audio_url
    except Exception as e:
        logger.critical("Could not extract the audio URL: {}".format(e))


def get_youtube_streams(url):
    """Get both audio & video stream urls for youtube using youtube-dl.

    PS: I don't know how youtube-dl does the magic
    """
    logger.debug("Extracting streamable links")
    logger.debug("{}".format(url))
    cli = "youtube-dl -g {}".format(url)
    output, error = exe(cli)
    logger.debug("{}".format(type(error)))

    if error != "":
        logger.critical(
            "'{}' Error passed by youtube-dl. Please check if the latest version of youtube-dl is installed. You can report the error on https://yt-dl.org/bug.".format(
                error
            )
        )

    logger.debug("O/P: {}".format(output))
    logger.debug("ERROR: {}".format(error))

    stream_urls = output.split("\n")
    url = {}
    try:
        url["audio"] = stream_urls[1]
    except IndexError:
        url["audio"] = None
    url["video"] = stream_urls[0]
    return url


def get_youtube_title(url):
    """
    Extract title of video from url.
    """
    return get_youtube_title2(url)

    """
    logger.debug("Extracting title of passed URL")
    try:
        r = requests.get(url)
    except Exception as e:
        logger.error("ERROR: {}".format(e))
        sys.exit(-1)
    title = re.findall(r"<title>.*?</title>", r.text)[0]
    title = re.sub(r"title|>|<|/|\ ?-|\ ?YouTube", "", str(title))
    return title
    """


def get_youtube_title2(url):
    """
    Extract the title of the video using youtube_dl
    """
    opts = {"quiet": True}
    ydl = youtube_dl.YoutubeDL(opts)
    data = ydl.extract_info(url, False)

    # Try to get the title
    try:
        title = data["title"]
    except KeyError:
        logger.error("Wasn't able to extract the title of the song.")

    return title


def add_better_search_kw(query):
    """
        Add some keywords to the search querry to get better results.
    """
    logger.debug("{}".format(query))
    if not is_song_url(query):
        for kw in better_search_kw:
            query += kw
    return query


def search_youtube(query, disable_kw=False):
    """Behold the greatest magic trick ever : crawl and crawl."""
    if not disable_kw:
        logger.debug(query)
        query = add_better_search_kw(query)
    logger.debug("Searching youtube for :: {}".format(query))
    base_url = "https://www.youtube.com"

    # Use youtube_search to search youtube for the query
    results = YoutubeSearch(query, max_results=10).to_dict()
    videos = []

    for result in results:
        youtube_metadata = YoutubeMetadata()
        youtube_metadata.title = result['title']
        youtube_metadata.url = base_url + result['url_suffix']
        youtube_metadata.duration = result['duration']
        videos.append(youtube_metadata)

    return videos


def grab_link(value):
    """Return the audio link of the song."""
    stream = get_audio_URL(value)
    logger.debug(stream)
    # if not no_cache:
    #    Cache.dw(value, title)
    return stream


def dw(title, s_url, url=None):
    # Start downloading
    title = fix_title(title)
    Cache.dw(s_url, title, url)


def main():
    """Run on program call."""
    url = "https://www.youtube.com/watch?v=erywPdFfORE"
    title = get_youtube_title(url)
    urls = get_youtube_streams(url)


if __name__ == "__main__":
    # main()
    search_youtube("Pehla nasha once again")
