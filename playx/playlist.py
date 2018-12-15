"""Youtube Playlist related functions."""

from requests import get
from bs4 import BeautifulSoup
import re
import os
from .youtube import YoutubeMetadata
from .billboard import Billboard

"""
__author__ = Deepjyoti Barman
__github__= github.com/deepjyoti30
"""


class YoutubePlaylist:
    """Class to store YouTube playlist data."""

    def __init__(self, URL, pl_start=None, pl_end=None):
        """Init the URl."""
        self.URL = URL
        self.data = []
        self.default_start = 1
        self.default_end = 0
        self.pl_start = pl_start
        self.pl_end = pl_end
        self.is_valid_start = False
        self.is_valid_end = False

    def extract_name(self, name):
        """Extract the name of the playlist."""
        name = str(name).replace('\n', '')
        name = ''.join(re.findall(r'>.*?<', name)).replace('>',
                                                           '').replace('<', '')
        name = ' '.join(re.findall(r'[^ ]+', name))
        return name

    def is_valid(self):
        """Check if pl_start and pl_end are valid."""
        self.is_valid_start = True if self.pl_start in range(
                                            self.default_start,
                                            self.default_end + 1) else False
        self.is_valid_end = True if self.pl_end in range(
                                            self.default_start,
                                            self.default_end + 1) else False

    def strip_to_start_end(self):
        """Strip the tuple to the positions passed by user."""
        # Before doing anything check if the passed numbers are valid
        self.is_valid()
        if self.pl_start is not None and self.is_valid_start:
            self.default_start = self.pl_start
        if self.pl_end is not None and self.is_valid_end:
            self.default_end = self.pl_end
        self.data = self.data[self.default_start - 1: self.default_end]

    def extract_playlistdata(self):
        """Extract all the videos into YoutubeMetadata objects."""
        url_prepend = 'https://www.youtube.com/watch?v='
        r = get(self.URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        name = soup.findAll('h1', attrs={'class': 'pl-header-title'})
        name = self.extract_name(name)
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
                youtube_metadata.duration = '0'
                self.data.append(youtube_metadata)

        if len(self.data) == 0:
            print("Are you sure you have videos in your playlist? Try changing\
                  privacy to public.")

        self.default_end = len(self.data)
        self.strip_to_start_end()
        return (name, self.data)


class Playxlist:
    """Class to store playx list data."""

    def __init__(self, file_path, pl_start=None, pl_end=None):
        """Init the path of the file."""
        self.file_path = file_path
        self.list_content_tuple = []
        self.default_start = 1
        self.default_end = 0
        self.pl_start = pl_start
        self.pl_end = pl_end
        self.is_valid_start = False
        self.is_valid_end = False

    def is_valid(self):
        """Check if pl_start and pl_end are valid."""
        self.is_valid_start = True if self.pl_start in range(
                                            self.default_start,
                                            self.default_end + 1) else False
        self.is_valid_end = True if self.pl_end in range(
                                            self.default_start,
                                            self.default_end + 1) else False

    def strip_to_start_end(self):
        """Strip the tuple to positions passed by the user."""
        # Before doing anything check if the passed numbers are valid
        self.is_valid()
        if self.pl_start is not None and self.is_valid_start:
            self.default_start = self.pl_start
        if self.pl_end is not None and self.is_valid_end:
            self.default_end = self.pl_end
        self.list_content_tuple = self.list_content_tuple[self.default_start - 1: self.default_end]

    def is_playx_list(self):
        """Check if the passed filepath is a playx playlist."""
        if not os.path.basename(self.file_path).endswith('.playx'):
            return False

        if not os.path.isfile(self.file_path):
            return False

        return True

    def extract_list_contents(self):
        """Get the stuff inside the file."""
        FILE_STREAM = open(self.file_path, 'r')

        while True:
            line = FILE_STREAM.readline()
            if not line:
                break
            self.list_content_tuple.append(line.replace('\n', ''))

        # Update the total length of the list_tuple
        self.default_end = len(self.list_content_tuple)

    def get_list_contents(self):
        """Return the tuple containing the list data."""
        self.extract_list_contents()
        self.strip_to_start_end()
        return self.list_content_tuple


class BillboardPlaylist:
    """Class to store Billboards Charts data."""

    def __init__(self, playlist_name, pl_start=None, pl_end=None):
        """Init the chart name."""
        self.playlist_name = playlist_name
        self.list_content_tuple = []
        self.pl_start = pl_start
        self.pl_end = pl_end
        self.default_start = 1
        self.default_end = 0
        self.is_valid_start = False
        self.is_valid_end = False

    def is_valid(self):
        """Check if pl_start and pl_end are valid."""
        self.is_valid_start = True if self.pl_start in range(
                                            self.default_start,
                                            self.default_end + 1) else False
        self.is_valid_end = True if self.pl_end in range(
                                            self.default_start,
                                            self.default_end + 1) else False

    def strip_to_start_end(self):
        """Strip the tuple to positions passed by the user."""
        # Before doing anything check if the passed numbers are valid
        self.is_valid()
        if self.pl_start is not None and self.is_valid_start:
            self.default_start = self.pl_start
        if self.pl_end is not None and self.is_valid_end:
            self.default_end = self.pl_end
        self.list_content_tuple = self.list_content_tuple[self.default_start - 1: self.default_end]

    def extract_list_contents(self):
        """Extract the playlist data."""
        Chart = Billboard(self.playlist_name)
        self.list_content_tuple = Chart.chart
        self.default_end = len(self.list_content_tuple)
        self.strip_to_start_end()
        self.playlist_name = Chart.chart_name


def is_playlist(url, type):
    """Check if the passed URL is a playlist."""
    if type.lower() == "youtube":
        playlist_part = 'https://www.youtube.com/playlist?list'
        if playlist_part in url:
            return True
        else:
            return False
    elif type.lower() == "billboard":
        billboard_URL = "https://www.billboard.com/charts/"
        response = get(billboard_URL + url)
        if response.status_code != 404:
            return True
        else:
            return False
