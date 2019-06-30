#!/usr/bin/env python3

"""
    This module is intended to use Markov Chains for generating playlist automatically.
    For now, simple counter is used to create a "naive" baseline auto-playlist.
"""

import pathlib
import re
import random
import numpy as np

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

class MarkovBasedAutoPlaylist(AbstractAutoPlaylist):
    """
        Treating each song as a node in a trie, next songs are generated based on
        probability of their occurences.

        For now, few songs are randomly selected (with weighted distribution).
        These songs act as seeds of some sort and we iteratively generate song songs
        using markov chain.
    """
    def __init__(self, log_path):
        super().__init__(log_path)

    def generate(self):
        data = self.get_timeseries_data(self.log_path)
        ts, songs = zip(*data)

        # build trie and probabilities
        pairs = list(zip(songs, songs[1:]))
        trie = self._build_trie(pairs)
        trie = self._build_probabilities(trie)

        counter = Counter(songs)
        songs_frequent, c = zip(*counter.most_common())
        result = []

        arr = np.array(c)
        # seed songs to use for markov chain
        songs_seed = list(set(random.choices(songs_frequent, arr/arr.sum(), k=20)))

        # for now only get 50 songs
        while len(result) < 50:
            # song = random.choices(songs_frequent, arr/arr.sum())[0].strip()
            for song in songs_seed:
                song = song.strip()
                result.append(song)
                res = self._generate(trie, initial_song=song, max_len=10, verbose=False)
                for r in res:
                    r = r.strip()
                    if r not in result:
                        result.append(r)
        self.data = result
        self.info()
        return result

    def _build_trie(self, pairs):
        trie = {}
        for pair in pairs:
            a, b = pair
            if a not in trie:
                trie[a] = {}
            if b not in trie[a]:
                trie[a][b] = 1
            else:
                trie[a][b] += 1
        return trie

    def _build_probabilities(self, trie):
        for word, following in trie.items():
            total = sum(following.values())
            for key in following:
                following[key] /= total
        return trie

    def _generate(self, trie, initial_song, max_len=5, verbose=True):
        res = []
        word = initial_song
        while len(res) < max_len:
            if word not in trie:
                break
            transitions = trie[word]
            if verbose:
                print("Current word :: ", word)
                print("Transitions :: ", transitions)
            t = 0
            for w in transitions:
                p = transitions[w]
                t += p
                if t and (random.random() * t) < p:
                    next_word = w
                if verbose:
                    print(w, p)
            res.append(word)
            word = next_word
        return res


def main():
    path = pathlib.Path("~/.playx/logs/log.cat").expanduser()

if __name__ == "__main__":
    main()

