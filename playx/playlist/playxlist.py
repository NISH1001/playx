"""Functions related to playxlist."""

import os

from playx.playlist.playlistmodder import (
    PlaylistBase
)


class Playxlist(PlaylistBase):
    """Class to store playx list data."""

    def __init__(self, file_path, pl_start=None, pl_end=None):
        """Init the path of the file."""
        super().__init__(pl_start, pl_end)
        self.file_path = file_path
        self.list_content_tuple = []

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
        PlaylistBase._update_end(self, len(self.list_content_tuple))
        PlaylistBase.list_content_tuple = self.list_content_tuple
        PlaylistBase._strip_to_start_end(self)

    def get_list_contents(self):
        """Return the tuple containing the list data."""
        self.extract_list_contents()
        self.strip_to_start_end()
        return self.list_content_tuple
