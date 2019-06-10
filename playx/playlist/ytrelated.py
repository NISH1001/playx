'''Scrap Youtube to get the related list from youtube'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from playx.playlist.playlistbase import (
    SongMetadataBase, PlaylistBase
)

from playx.logger import Logger

logger = Logger('YoutubeRelated')


class YoutubeMetadata(SongMetadataBase):
    """
    Class to hold contents of the playlist.
    """
    def __init__(self, title):
        super().__init__()
        self.title = title
        self._create_search_querry()

    def _create_search_querry(self):
        """
        Create a search querry.
        """
        self.search_querry = self.title


class YoutubeRelatedIE(PlaylistBase):
    """Youtube Related songs extractor."""

    def __init__(self, url):
        super().__init__()
        self.url = url

    def extract_songs(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options)

        driver.implicitly_wait(30)
        driver.get(self.url)
        songs = driver.find_elements_by_tag_name('ytd-compact-video-renderer')
        logger.debug(str(len(songs)))

        for i in songs:
            contents = i.text.split('\n')
            song_name = contents[0]
            logger.debug(song_name)
            self.list_content_tuple.append(YoutubeMetadata(song_name))

        driver.quit()


def get_data(url):
    logger.debug("Extracting related songs")
    youtube_related = YoutubeRelatedIE(url)
    youtube_related.extract_songs()
    return youtube_related.list_content_tuple


if __name__ == '__main__':
    print(str(get_data('https://www.youtube.com/watch\?v\=by3yRdlQvzs')))
