"""Functions related to jiosaavn."""

from playx.playlist.playlistbase import (
    PlaylistBase, SongMetadataBase
)

from selenium import webdriver
import re

from playx.logger import (
    Logger
)

# Setup logger
logger = Logger('JioSaavn')


class SongMetadata(SongMetadataBase):

    def __init__(self, title='', subtitle=''):
        super().__init__()
        self.title = title
        self.subtitle = subtitle
        self._create_search_querry()
        self._remove_duplicates()

    def _create_search_querry(self):
        """
        Create a search querry.
        """
        self.search_querry = self.title + ' ' + self.subtitle


class JioSaavnIE(PlaylistBase):
    """
    Class to extract information from playlist
    of JioSaavn.

    The pages use javascript to load the data later
    thus selenium is used.
    """

    def __init__(self, URL, is_shuffle, pl_start=None, pl_end=None):
        super().__init__(pl_start, pl_end)
        self.URL = URL
        self.list_content_tuple = []
        self.playlist_name = ''
        self.is_shuffle = is_shuffle

    def get_data(self):
        """
        Get the data from the page.
        """
        driver = webdriver.PhantomJS()
        driver.get(self.URL)
        for i in driver.find_elements_by_class_name('song-wrap'):
            data = i.text.split('\n')
            title = re.sub(r'-|,', '', data[2])
            subtitle = re.sub(r'-|,', '', data[3])
            self.list_content_tuple.append(SongMetadata(title, subtitle))

        self.strip_to_start_end()

        playlist = driver.find_elements_by_class_name('meta-info')[0]
        playlist = playlist.text.split('\n')[0]
        self.playlist_name = playlist

        if self.is_shuffle:
            self.shufflelist()


def get_data(URL, pl_start, pl_end, shuffle):
    """Generic function. Should be called only when
    it is checked if the URL is a jiosaavn playlist.

    Returns a tuple containing the songs and name of
    the playlist.
    """

    logger.info('Extracting Playlist Content')
    jio_saavn_IE = JioSaavnIE(URL, shuffle, pl_start, pl_end)
    jio_saavn_IE.get_data()
    return jio_saavn_IE.list_content_tuple, jio_saavn_IE.playlist_name
