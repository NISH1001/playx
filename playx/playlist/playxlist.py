"""Functions related to playxlist."""

import os
import random

from playx.playlist.playlistbase import PlaylistBase

from loguru import logger

# from playx.logger import Logger

# Setup logger
# logger = Logger("Playxlist")


class Playxlist(PlaylistBase):
    """Class to store playx list data."""

    def __init__(self, content, pl_start=None, pl_end=None, shuffle=False):
        """
            Initialize with either filepath or content.
            Content represent either filepath or list of song names
        """
        super().__init__(pl_start, pl_end, shuffle=shuffle)
        if type(content) is list:
            self.file_path = None
            self.list_content_tuple = content
        if type(content) is str:
            self.list_content_tuple = []
            self.file_path = content

    def is_playx_list(self):
        """Check if the passed filepath is a playx playlist."""
        if self.list_content_tuple and not self.file_path:
            return True
        if not os.path.basename(self.file_path).endswith(".playx"):
            return False
        if not os.path.isfile(self.file_path):
            return False
        return True

    def extract_list_contents(self):
        """Get the stuff inside the file."""
        if self.list_content_tuple and not self.file_path:
            return
        with open(self.file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    self.list_content_tuple.append(line)

    def get_list_contents(self):
        """Return the tuple containing the list data."""
        logger.log("FLOG", "Extracting Playlist Content")
        self.extract_list_contents()
        self.strip_to_start_end()
        data = self.list_content_tuple
        if self.file_path:
            logger.log(
                "FLOG",
                "{}: {} {}".format(
                    self.file_path, len(data), "song" if len(data) < 2 else "songs"
                ),
            )
        else:
            logger.log(
                "FLOG", "{} {}".format(len(data), "song" if len(data) < 2 else "songs")
            )
        if self.shuffle:
            logger.log("FLOG", "Shuffling...")
            random.shuffle(self.list_content_tuple)
        return self.list_content_tuple
