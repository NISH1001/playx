"""Youtube playlist related functions and classes
defined.
"""

import json
import requests
from bs4 import BeautifulSoup
import re

from playx.utility import exe

from playx.playlist.playlistbase import PlaylistBase, SongMetadataBase

from playx.logger import Logger


# Setup logger
logger = Logger("YoutubePlaylist")


class YoutubeMetadata(SongMetadataBase):
    def __init__(self, url="", title=""):
        super().__init__(title, url, "")
        self._create_search_query()

    def _create_search_query(self):
        """
        Create a search querry.
        """
        self.search_query = self.URL

    def display(self):
        """Be informative."""
        logger.info("Title: {}".format(self.title))


class YoutubePlaylist(PlaylistBase):
    """
        Class to store YouTube playlist data.
        This is where we try to parse ourselves the results of the pages.
        Only works for first 100 songs.
        If we want to fetch more, we have to do other ajax request or simulate
        scrolling which is another problem.
        Refer to `YoutubePlaylist2`
    """

    def __init__(self, URL, pl_start=None, pl_end=None):
        """Init the URl."""
        super().__init__(pl_start, pl_end)
        self.URL = URL
        self.list_content_tuple = []
        self.playlist_name = ""
        self._DELETED = [
            "deleted video",
            "मेटाइएको भिडियो",
            "private video",
        ]

    def extract_name(self, name):
        """Extract the name of the playlist."""
        name = str(name).replace("\n", "")
        name = "".join(re.findall(r">.*?<", name)).replace(">", "").replace("<", "")
        name = " ".join(re.findall(r"[^ ]+", name))
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

    def _check_valid(self, url):
        """Check if the passed URL is valid."""
        h = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux \
            x86_64; rv:49.0) Gecko/20100101 Firefox/49.0"
        }
        s = BeautifulSoup(requests.get(url, headers=h).text, "lxml")
        t = 'window["ytInitialData"] = '
        i = next((i for i in s.find_all("script") if t in str(i)))
        i = i.get_text().replace(t, "").replace("\n", "")
        i = re.sub(r'^.*"playabilityStatus"', "", i)
        i = i.split(",")
        status = re.sub(r':|\{|"|status', "", i[0])
        if status == "OK":
            return True
        else:
            reason = next((r for r in i if '"reason"' in r))
            reason = re.sub(r':|\{|"|reason|simpleText|}', "", reason)
            logger.info("Skipping {}: {} {}".format(url, status, reason))
            return False

    def extract_playlistdata(self):
        """Extract all the videos into YoutubeMetadata objects."""
        url_prepend = "https://www.youtube.com/watch?v="
        url_base = "https://www.youtube.com"
        if not self._is_connection_possible():
            logger.warning("Cannot play playlist. No connection detected!")
            return "N/A", []
        r = requests.get(self.URL)
        soup = BeautifulSoup(r.text, "html.parser")
        name = soup.findAll("h1", attrs={"class": "pl-header-title"})
        self.extract_name(name)
        # soup = soup.findAll('tr', attrs={'class': 'pl-video',
        #                                  'class': 'yt-uix-tile'})
        logger.debug(len(soup))

        # use regex to get video url
        # this seems rigid against <div> changes
        # so, far this works
        links = soup.find_all(
            "a", href=re.compile(r".*watch.*")  # this regex can be improved in future
        )
        for link in links:
            href = link["href"]
            title = link.contents[0]
            # If the link is not a video from playlist, there will be no
            # 'index' substring. Hence, we can skip this
            if "index" not in href:
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
            # Check if the video is deleted. Some videos in playlist turn out
            # to be deleted videos. We can put a check for that by checking
            # if the title is [Deleted video]
            # We have a simpler way to check for deleted videos
            if title.lower()[1:-1] in self._DELETED:
                logger.debug(title.lower()[1:-1])
                logger.info("Skipping {}: DELETED/BLOCKED/PRIVATE video.".format(url))
                continue

            if not self._check_valid(url):
                continue

            self.list_content_tuple.append(YoutubeMetadata(url, title))

        if len(self.list_content_tuple) == 0:
            logger.warning(
                "Are you sure you have videos in your playlist? Try changing\
                  privacy to public."
            )

        self.strip_to_start_end()

    def _get_url_slicer(self, url):
        slicers = []
        strings = ["&index=", "&t=", "&list="]
        for s in strings:
            try:
                slicer = url.index(s)
                slicers.append(slicer)
            except ValueError:
                continue
        return min(slicers)


class YoutubePlaylist2(PlaylistBase):
    """
        Class to store YouTube playlist data.
        This uses youtube-dl --flat-playlist command to fetch everything.
        This is more robust since we don't have to manually parse everything.
        Plus this solves the issue with ajax/scrolling if playlist has more than
        100 songs.
    """

    def __init__(self, URL, pl_start=None, pl_end=None):
        """Init the URl."""
        super().__init__(pl_start, pl_end)
        self.URL = URL
        self.list_content_tuple = []
        self.playlist_name = ""
        self._DELETED = [
            "deleted video",
            "मेटाइएको भिडियो",
            "private video",
        ]

    def extract_name(self, name):
        """Extract the name of the playlist."""
        name = str(name).replace("\n", "")
        name = "".join(re.findall(r">.*?<", name)).replace(">", "").replace("<", "")
        name = " ".join(re.findall(r"[^ ]+", name))
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
        url_prepend = "https://www.youtube.com/watch?v="
        url_base = "https://www.youtube.com"
        if not self._is_connection_possible():
            logger.warning("Cannot play playlist. No connection detected!")
            return "N/A", []

        # first get playlist name
        logger.info(f"Fetching playlist name for [{self.URL}]")
        r = requests.get(self.URL)
        soup = BeautifulSoup(r.text, "html.parser")
        name = soup.findAll("h1", attrs={"class": "pl-header-title"})
        self.extract_name(name)
        logger.info(f"Playlist name = [{self.playlist_name}]")

        logger.info("Fetching songs...")
        cmd = f"youtube-dl -j --flat-playlist {self.URL}"
        output, errors = exe(cmd)
        if not output and errors:
            logger.error("Unable to extract playlist")
            return "N/A", []
        videos = list(map(json.loads, output.split("\n")))
        logger.info(f"Found {len(videos)} songs")
        for i, video in enumerate(videos):
            title = video["title"].strip()
            url = video["url"]
            url = url_prepend + url
            if title.lower()[1:-1] in self._DELETED:
                logger.debug(title.lower()[1:-1])
                logger.info(f"Skipping [{url}] Possibly DELETED/BLOCKED/PRIVATE video.")
                continue
            self.list_content_tuple.append(YoutubeMetadata(url, title))
        if len(self.list_content_tuple) == 0:
            logger.warning(
                "Are you sure you have videos in your playlist? Try changing\
                  privacy to public."
            )
        self.strip_to_start_end()

        if len(self.list_content_tuple) == 0:
            logger.warning(
                "Are you sure you have videos in your playlist? Try changing\
                  privacy to public."
            )
        self.strip_to_start_end()


def get_data(URL, pl_start, pl_end):
    """Generic function. Should be called only when
    it is checked if the URL is a youtube playlist.

    Returns a tuple containing the songs and name of
    the playlist.
    """

    logger.debug("Extracting Playlist Content")
    youtube_playlist = YoutubePlaylist2(URL, pl_start, pl_end)
    youtube_playlist.extract_playlistdata()

    return youtube_playlist.list_content_tuple, youtube_playlist.playlist_name


def main():
    url = "https://www.youtube.com/playlist?list=PLwg22VSCR0W6cwuCKUJSkX72xEvYXS0Zx"
    print(url)

    yp = YoutubePlaylist2(url)
    yp.extract_playlistdata()


if __name__ == "__main__":
    main()
