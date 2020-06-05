"""Functions related to jiosaavn."""

from playx.playlist.playlistbase import PlaylistBase, SongMetadataBase

from bs4 import BeautifulSoup
import requests
from json import JSONDecoder
import re

from playx.logger import Logger

# Setup logger
logger = Logger("JioSaavn")


class SongMetadata(SongMetadataBase):
    def __init__(self, title="", subtitle=""):
        super().__init__()
        self.title = title
        self.subtitle = subtitle
        self._create_search_query()
        self._remove_duplicates()

    def _create_search_query(self):
        """
        Create a search querry.
        """
        self.search_query = self.title + " " + self.subtitle


class JioSaavnIE(PlaylistBase):
    """
    Class to extract information from playlist
    of JioSaavn.

    The pages use javascript to load the data later
    thus selenium is used.
    """

    def __init__(self, URL, pl_start=None, pl_end=None):
        super().__init__(pl_start, pl_end)
        self.URL = URL
        self._headers = {
            "User-Agent": "Mozilla/5.0 \
                                   (X11; Ubuntu; Linux x86_64; rv:49.0)\
                                   Gecko/20100101 Firefox/49.0"
        }
        self.list_content_tuple = []
        self.playlist_name = ""

    def get_data(self):
        """
        Get the data from the page.
        """
        response = requests.get(self.URL, headers=self._headers)
        soup = BeautifulSoup(response.text, "lxml")
        songs = soup.find_all("div", {"class": "hide song-json"})

        for i in songs:
            obj = JSONDecoder().decode(i.text)
            self.list_content_tuple.append(SongMetadata(obj["title"], obj["singers"]))

        self.strip_to_start_end()

        # Extract the name of the playlist
        self.playlist_name = soup.find_all("h1", {"class": "page-title ellip"})
        self.playlist_name = re.findall(r">.*?<", str(self.playlist_name))[0]
        self.playlist_name = re.sub(r">|<", "", self.playlist_name)


def get_data(URL, pl_start, pl_end):
    """Generic function. Should be called only when
    it is checked if the URL is a jiosaavn playlist.

    Returns a tuple containing the songs and name of
    the playlist.
    """

    logger.debug("Extracting Playlist Content")
    jio_saavn_IE = JioSaavnIE(URL, pl_start, pl_end)
    jio_saavn_IE.get_data()
    return jio_saavn_IE.list_content_tuple, jio_saavn_IE.playlist_name
