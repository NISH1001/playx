"""Youtube playlist related functions and classes
defined.
"""

import requests
from bs4 import BeautifulSoup
import re

from playx.playlist.playlistbase import (
    PlaylistBase, SongMetadataBase
)

from playx.logger import Logger


# Setup logger
logger = Logger('YoutubePlaylist')


class YoutubeMetadata(SongMetadataBase):

    def __init__(self, url='', title=''):
        super().__init__()
        self.URL = url
        self.title = title
        self._create_search_querry()

    def _create_search_querry(self):
        """
        Create a search querry.
        """
        self.search_querry = self.URL

    def display(self):
        """Be informative."""
        logger.info("Title: {}".format(self.title))


class YoutubePlaylist(PlaylistBase):
    """Class to store YouTube playlist data."""

    def __init__(self, URL, pl_start=None, pl_end=None):
        """Init the URl."""
        super().__init__(pl_start, pl_end)
        self.URL = URL
        self.list_content_tuple = []
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
        url_base = 'https://www.youtube.com'
        if not self._is_connection_possible():
            logger.warning("Cannot play playlist. No connection detected!")
            return 'N/A', []
        r = requests.get(self.URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        name = soup.findAll('h1', attrs={'class': 'pl-header-title'})
        self.extract_name(name)
        # soup = soup.findAll('tr', attrs={'class': 'pl-video',
        #                                  'class': 'yt-uix-tile'})
        logger.debug(len(soup))

        # use regex to get video url
        # this seems rigid against <div> changes
        # so, far this works
        links = soup.find_all(
            'a',
            href=re.compile(r".*watch.*") # this regex can be improved in future
        )
        for link in links:
            href = link['href']
            title = link.contents[0]
            # If the link is not a video from playlist, there will be no
            # 'index' substring. Hence, we can skip this
            if 'index' not in href:
                continue
            # Just to make sure the title is not empty. This is done because
            # there is always a first link that contains 'index', yet does not
            # have a title. This represents the meta-link: a link to playlist
            # itself.
            title = title.strip()
            if not title:
                continue
            # Get video url using simple algorithm. This 3 index search is done
            # just to make sure when youtube playlist url has these query
            # params in shuffled order.
            slicer = self._get_url_slicer(href)
            url = url_base + href[:slicer]
            self.list_content_tuple.append(YoutubeMetadata(url, title))
        # for i in soup:
        #     a = re.findall(r'class="pl-video yt-uix-tile".*?data-title=.*?data-video-id=.*?>', str(i))
        #     video_title = re.findall(r'data-title=".*?"', a[0])
        #     video_id = re.findall(r'data-video-id=".*?"', a[0])
        #     if len(video_title) != 0 and len(video_id) != 0:
        #         video_title = video_title[0].replace("data-title=", '').replace('"', '')
        #         video_id = video_id[0].replace("data-video-id=", '').replace('"', '')
        #         url = url_prepend + video_id
        #         title = video_title
        #         self.list_content_tuple.append(YoutubeMetadata(url, title))

        if len(self.list_content_tuple) == 0:
            logger.warning("Are you sure you have videos in your playlist? Try changing\
                  privacy to public.")

        self.strip_to_start_end()

    def _get_url_slicer(self, url):
        slicers = []
        strings = ['&index=', '&t=', '&list=']
        for s in strings:
            try:
                slicer = url.index(s)
                slicers.append(slicer)
            except ValueError:
                continue
        return min(slicers)


def get_data(URL, pl_start, pl_end):
    """Generic function. Should be called only when
    it is checked if the URL is a youtube playlist.

    Returns a tuple containing the songs and name of
    the playlist.
    """

    logger.info("Extracting Playlist Content")
    youtube_playlist = YoutubePlaylist(URL, pl_start, pl_end)
    youtube_playlist.extract_playlistdata()

    return youtube_playlist.list_content_tuple, youtube_playlist.playlist_name
