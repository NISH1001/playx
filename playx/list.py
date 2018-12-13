"""Functions related to playing from a list are definded here."""

import os


class Playxlist():
    """Class to store playx list data."""

    def __init__(self, file_path, pl_start=None, pl_end=None):
        self.file_path = file_path
        self.list_content_tuple = []
        self.pl_start = pl_start
        self.pl_end = pl_end

    def strip_to_start_end(self):
        if self.pl_start is not None:
            index = self.pl_start - 1
            try:
                self.list_content_tuple = self.list_content_tuple[index:]
            except IndexError:
                pass
        if self.pl_end is not None:
            index = self.pl_end - 1
            try:
                self.list_content_tuple = self.list_content_tuple[:index]
            except IndexError:
                pass

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

    def get_list_contents(self):
        """Return the tuple containing the list data."""
        self.extract_list_contents()
        self.strip_to_start_end()
        return self.list_content_tuple
