"""Scrap Youtube to get the related list from youtube"""

import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from pathlib import Path
import json

from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError

from playx.playlist.playlistbase import SongMetadataBase, PlaylistBase

from playx.logger import Logger

logger = Logger("YoutubeRelated")


class YoutubeMetadata(SongMetadataBase):
    def __init__(self, url=None):
        super().__init__()
        self.url = url
        self._create_search_query()

    def _create_search_query(self):
        """
        Update the search query using the passed URL.
        """
        self.search_query = self.url


class CustomYTDLLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


class YoutubeRelatedIE(PlaylistBase):
    """
    Get related songs using the YT music endpoint that
    automatically creates a mix based on the song.

    We STRICTLY need a video ID or and YoutubeURL, a name
    won't work.
    """

    def __init__(self, url):
        super().__init__()
        self.url = url
        # self.url = self._update_URL(URL)
        self.playlist_name = ""
        self.youtube_base = "https://www.youtube.com/watch?v={}"

    def _get_ytmusic_url(self, url):
        """
        Get the video ID from the URL and add it to
        the YoutubeMusic base URL.
        """
        video_id = url.split("=")[-1]
        return "https://music.youtube.com/watch?v={}".format(video_id)

    def _get_playlist_data(self, url):
        """
        Use YoutubeDL to extract all the songs from the
        passed URL.
        """
        ydl_opts = {
            "quiet": True,
            "nocheckcertificate": True,
            "dump_single_json": True,
            "extract_flat": True,
            "logger": CustomYTDLLogger(),
        }

        # Extract the info now
        songs = YoutubeDL(ydl_opts).extract_info(url, False)

        # Extract the songs into the MetaData class' objects
        for song in songs["entries"]:
            self.list_content_tuple.append(YoutubeMetadata(song["url"]))
        self.playlist_name = songs["title"]

    def _create_mix(self):
        """
        In order to get the playlist, we need to make a request
        to youtube music.
        YT Music uses JS to automatically update the page URL with
        the playlist ID.
        This is when we extract the list ID.

        Since it does all of it using JS, we can't use requests or
        someting similar.
        """
        logger.info("Using YTMusic Method")
        logger.debug(self.url)
        driver = self._get_driver()
        driver.get(self.url)

        try:
            WebDriverWait(driver, 10).until(
                lambda driver: driver.current_url != self.url
            )
        except TimeoutException:
            raise DownloadError("Timeout exception occurred")

        # The URL should now be updated
        updated_url = driver.current_url
        playlist_id = updated_url.split("=")[-1]
        playlist_url = "https://www.youtube.com/playlist?list={}".format(playlist_id)
        self._get_playlist_data(playlist_url)

    def _not_name(self, name):
        """
        Check the passed name to see if its actually a name of song.

        While extracting sometimes playlists are suggested in which
        the extraction algo extracts the time of the playlist instead
        of the name, so we need to remove it from the list of songs.
        """
        match = re.match(r"[0-9][0-9]?:[0-9][0-9]", name)
        if match is None:
            return False
        else:
            return True

    def _get_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("–disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        return webdriver.Chrome(options=chrome_options)

    def _extract_fallback(self):
        logger.info("Using fallback method")
        driver = self._get_driver()
        driver.implicitly_wait(10)
        driver.get(self.url)
        songs = driver.find_elements_by_tag_name("ytd-compact-video-renderer")
        logger.debug(str(len(songs)))

        for i in songs:
            contents = i.text.split("\n")
            song_name = contents[0]
            logger.debug(song_name)
            if not self._not_name(song_name):
                self.list_content_tuple.append(YoutubeMetadata(song_name))
        driver.quit()

    def extract_songs(self):
        """
        Generic method to start all the fetching related work.
        """
        original_url = self.url
        try:
            self.url = self._get_ytmusic_url(original_url)
            self._create_mix()
        except DownloadError:
            self.url = original_url
            self._extract_fallback()


def get_data(url):
    logger.debug("Extracting related songs")
    logger.debug("Checking if file is present.")

    CACHE_PATH = Path("~/.playx/playlist").expanduser()
    FILE_NAME = "related_{}.json".format(url.split("\\=")[-1])
    FILE_PATH = CACHE_PATH.joinpath(Path(FILE_NAME))

    logger.debug("Checking related playlist cache")
    # Check if FILE_NAME is present in CACHE_PATH
    for fname in CACHE_PATH.iterdir():
        logger.debug("{}".format(fname))
        if fname == FILE_PATH:
            # Extract the data from FILE_PATH
            with open(FILE_PATH) as RSTREAM:
                data = json.load(RSTREAM)[1]["data"]
                data_ = []
                for title in data:
                    data_.append(YoutubeMetadata(title))
            return data_

    logger.info("Fetching data online")
    youtube_related = YoutubeRelatedIE(url)
    youtube_related.extract_songs()
    logger.debug("Saving the data...")
    logger.debug(str(len(youtube_related.list_content_tuple)))

    if len(youtube_related.list_content_tuple):
        save_data(url, youtube_related.list_content_tuple)

    return youtube_related.list_content_tuple


def save_data(url, data):
    """
    Save the data in a json file so that it can be accessed later.
    """
    CACHE_PATH = Path("~/.playx/playlist").expanduser()
    FILE_NAME = "related_{}.json".format(url.split("=")[-1])
    FILE_PATH = CACHE_PATH.joinpath(Path(FILE_NAME))

    FILE_PATH.touch()

    # Make the data a bit proper
    data_ = []
    for entity in data:
        data_.append(entity.title if entity.title else entity.search_query)

    with open(FILE_PATH, "w") as WSTREAM:
        DATA = [{"URL": url}, {"data": data_}]
        json.dump(DATA, WSTREAM)


if __name__ == "__main__":
    print("Debugging ytrelated...")
    url = "https://www.youtube.com/watch?v=fdubeMFwuGs"
    # url = "https://www.youtube.com/watch?v=bSxJp3dE0HY"
    print(f"url = {url}")
    d = get_data(url)
    for i in d:
        print(i.url)
