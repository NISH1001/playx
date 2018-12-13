"""Functions related to playing from a list are definded here."""

import os


class Playxlist():
    """Class to store playx list data."""

    def __init__(self, file_path):
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

    def get_list_contents(self):
        """Return the tuple containing the list data."""
        self.extract_list_contents()
        return self.list_content_tuple
