"""File to modify the playlists."""

from playx.logger import (
    get_logger
)


# Setup logger
logger = get_logger('playlistmodder')


class PlaylistBase():
    """Strip the playlist according to the passed index."""

    def __init__(self, pl_start, pl_end):
        self.pl_start = pl_start
        self.pl_end = pl_end
        self.default_start = 1
        self.default_end = 0
        self.is_valid_start = False
        self.is_valid_end = False
        self.list_content_tuple = []

    def _is_valid(self):
        """Check if pl_start and pl_end are valid."""
        self.is_valid_start = True if self.pl_start in range(
                                            self.default_start,
                                            self.default_end + 1) else False
        self.is_valid_end = True if self.pl_end in range(
                                            self.default_start,
                                            self.default_end + 1) else False

    def strip_to_start_end(self):
        """Strip the tuple to positions passed by the user."""
        # Before doing anything check if the passed numbers are valid
        self.default_end = len(self.list_content_tuple)
        logger.debug('{}: {} {}'.format(self.pl_start, self.pl_end, self.default_end))
        self._is_valid()
        if self.pl_start is not None and self.is_valid_start:
            self.default_start = self.pl_start
        if self.pl_end is not None and self.is_valid_end:
            self.default_end = self.pl_end
        self.list_content_tuple = self.list_content_tuple[self.default_start - 1: self.default_end]
