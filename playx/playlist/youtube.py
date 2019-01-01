"""Youtube playlist related functions and classes
defined.
"""

import requests
from bs4 import BeautifulSoup
import re

from playx.playlist.playlistmodder import (
    PlaylistBase
)

from playx.logger import get_logger


# Setup logger
logger = get_logger('YoutubePlaylist')


class YoutubeMetadata():

    def __init__(self):
        self.URL = ''
        self.title = ''

    def display(self):
        """Be informative."""
        logger.info("Title: {}".format(self.title))


class YoutubePlaylist(PlaylistBase):
    """Class to store YouTube playlist data."""

    def __init__(self, URL, pl_start=None, pl_end=None):
        """Init the URl."""
        super().__init__(pl_start, pl_end)
        self.URL = URL
        self.data = []
        self.playlist_name = ''

    def extract_name(self, name):
        """Extract the name of the playlist."""
        name = str(name).replace('\n', '')
        name = ''.join(re.findall(r'>.*?<', name)).replace('>',
                                                           '').replace('<', '')
        name = ' '.join(re.findall(r'[^ ]+', name))
        self.playlist_name = name

    def _is_connection_possible(self):
        """Make a simple request to check if connection is possible.
        i:e check if internet is connected.
        """
        url = "https://google.com"
        try:
            requests.get(url)
        except requests.exceptions.ConnectionError:
            return False

        return True

    def extract_playlistdata(self):
        """Extract all the videos into YoutubeMetadata objects."""
        url_prepend = 'https://www.youtube.com/watch?v='
        if not self._is_connection_possible():
            logger.warning("Cannot play playlist. No connection detected!")
            return 'N/A', []
        r = requests.get(self.URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        name = soup.findAll('h1', attrs={'class': 'pl-header-title'})
        self.extract_name(name)
        soup = soup.findAll('tr', attrs={'class': 'pl-video',
                                         'class': 'yt-uix-tile'})

        for i in soup:
            a = re.findall(r'class="pl-video yt-uix-tile ".*?data-title=.*?data-video-id=.*?>', str(i))
            video_title = re.findall(r'data-title=".*?"', a[0])
            video_id = re.findall(r'data-video-id=".*?"', a[0])
            if len(video_title) != 0 and len(video_id) != 0:
                video_title = video_title[0].replace("data-title=", '').replace('"', '')
                video_id = video_id[0].replace("data-video-id=", '').replace('"', '')
                youtube_metadata = YoutubeMetadata()
                youtube_metadata.url = url_prepend + video_id
                youtube_metadata.title = video_title
                self.data.append(youtube_metadata)

        if len(self.data) == 0:
            logger.warning("Are you sure you have videos in your playlist? Try changing\
                  privacy to public.")

        PlaylistBase._update_end(self, len(self.data))
        PlaylistBase.list_content_tuple = self.data
        PlaylistBase._strip_to_start_end(self)


def get_data(URL, pl_start, pl_end):
    """Generic function. Should be called only when
    it is checked if the URL is a youtube playlist.

    Returns a tuple containing the songs and name of
    the playlist.
    """

    youtube_playlist = YoutubePlaylist(URL, pl_start, pl_end)
    youtube_playlist.extract_playlistdata()

    return youtube_playlist.data, youtube_playlist.playlist_name
