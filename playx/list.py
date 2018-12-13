"""Functions related to playing from a list are definded here."""

import os


class Playxlist():
    """Class to store playx list data."""

    def __init__(self, file_path, pl_start=None, pl_end=None):
        self.file_path = file_path
        self.list_content_tuple = []
        self.default_end = 1
        self.default_start = 0
        self.pl_start = pl_start
        self.pl_end = pl_end
        self.is_valid_start = False
        self.is_valid_end = False

    def is_valid(self):
        """Check if pl_start and pl_end are valid."""
        self.is_valid_start = True if self.pl_start in range(self.default_start,
                                    self.default_end) else False
        self.is_valid_end = True if self.pl_end in range(self.default_start,
                                    self.default_end) else False

    def strip_to_start_end(self):
        # Before doing anything check if the passed numbers are valid
        self.is_valid()
        if self.pl_start is not None and self.is_valid_start:
            self.default_start = self.pl_start
        if self.pl_end is not None and self.is_valid_end:
            self.default_end = self.pl_end
        self.list_content_tuple = self.list_content_tuple[self.default_start - 1: self.default_end]

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
        self.default_end = len(self.list_content_tuple)

    def get_list_contents(self):
        """Return the tuple containing the list data."""
        self.extract_list_contents()
        self.strip_to_start_end()
        return self.list_content_tuple
