#!/usr/bin/env python3

"""
    This module is intended to use Markov Chains for generating playlist automatically.
    For now, simple counter is used to create a "naive" baseline auto-playlist.
"""

import pathlib
import re

from collections import Counter

from abc import (
    ABC, abstractmethod
)

from playx.stringutils import (
    remove_multiple_spaces,
    remove_punct
)
from playx.logger import Logger

logger = Logger('autoplaylist')

class AbstractAutoPlaylist(ABC):
    def __init__(self, log_path):
        self.log_path = pathlib.Path(log_path).expanduser()
        self.data = []

    @abstractmethod
    def generate(self):
        """
            Override this method to create any arbitary playlist
        """
        pass

    def info(self):
        logger.info("Auto-Generating playlist with [{}] songs using [{}]".format(
            len(self.data), self.__class__.__name__
        ))

    def get_timeseries_data(self, log_path):
        data = []
        with open(log_path) as f:
            for line in f:
                line = line.strip().lower()
                if 'playing' not in line:
                    continue
                matches = re.findall(r"\[.*?\]", line)
                module, timestamp = matches[0], matches[1]
                try:
                    song = matches[2]
                    ts = re.sub(r"[\[\]]+", '', timestamp)
                    song = re.sub(r"[\[\]]+", '', song)
                    song = remove_punct(song)
                    song = remove_multiple_spaces(song)
                    data.append((ts, song))
                except IndexError:
                    continue
        return data

class CountBasedAutoPlaylist(AbstractAutoPlaylist):
    """
        A very simple auto playlist that makes use of frequency of the songs
        in the logs.
    """
    def __init__(self, log_path):
        super().__init__(log_path)

    def generate(self):
        data = self.get_timeseries_data(self.log_path)
        ts, songs = zip(*data)
        counter = Counter(songs)
        songs_frequent, c = zip(*counter.most_common())
        self.data = songs_frequent
        self.info()
        return list(songs_frequent)

    def write_to_file(self, songs, path):
        outpath = pathlib.Path(path).expanduser()
        with open(outpath, 'w') as f:
            for s in songs:
                f.write("{}\n".format(s))
        return outpath


def main():
    path = pathlib.Path("~/.playx/logs/log.cat").expanduser()

if __name__ == "__main__":
    main()

