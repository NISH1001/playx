"""Youtube music playlist related functions and classes
defined.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from playx.playlist.playlistbase import (
    PlaylistBase, SongMetadataBase
)

from playx.logger import Logger

# Setup logger
logger = Logger("YouTubeMusic")


class YtMusicMetadata(SongMetadataBase):
    """Store data of YouTube Music songs."""

    def __init__(self, url='', title='', artist=''):
        super().__init__()
        self.URL = url
        self.title = title
        self.artist = artist
        self._create_querry()

    def _create_querry(self):
        self.search_querry = self.title + ' ' + self.artist


class YtMusicPlaylist(PlaylistBase):
    """Extract YouTube Music playlists."""

    def __init__(self, URL, pl_start=None, pl_end=None):
        super().__init__(pl_start=pl_start, pl_end=pl_end)
        self.URL = URL
        self.list_content_tuple = []
        self.playlist_name = None
        self._preprocess_driver()

    def _preprocess_driver(self):
        """Do all the stuff required for the driver."""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.URL)

    def _extract_name(self):
        """Extract the name of the playlist."""
        meta = self.driver.find_element_by_class_name('metadata')
        self.playlist_name = meta.find_element_by_class_name('title').text

    def _extract_songs(self):
        """Extract the songs."""

        # Get all the songs first.
        songs = self.driver.find_elements_by_class_name('flex-columns')

        for song in songs:
            URL = song.find_element_by_tag_name('a').get_attribute('href')
            title = song.find_element_by_class_name('title').text
            artist = song.find_element_by_class_name('flex-column').text
            self.list_content_tuple.append(YtMusicMetadata(
                                URL, title, artist
                            ))

        self.strip_to_start_end()

    def extract_data(self):
        """Extract the data by calling the other extract functions."""
        self._extract_name()
        self._extract_songs()


def get_data(URL, pl_start, pl_end):
    """Generic function. Should be called only when
    it is checked if the URL is a youtube playlist.

    Returns a tuple containing the songs and name of
    the playlist.
    """

    logger.debug("Extracting Playlist Content")
    ytmusic_playlist = YtMusicPlaylist(URL, pl_start, pl_end)
    ytmusic_playlist.extract_data()

    return ytmusic_playlist.list_content_tuple, ytmusic_playlist.playlist_name
