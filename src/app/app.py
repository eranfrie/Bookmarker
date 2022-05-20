from pathlib import Path
import logging

from utils.html_utils import html_escape
from server.server_api import InternalException, TitleRequiredException, URLRequiredException
from app.app_sections import DisplayBookmarksSection, AddBookmarkSection, StatusSection


GET_BOOKMARKS_ERR_MSG = "Internal error. Please try again later"
ADD_BOOKMARK_ERR_MSG = "Internal error: Failed to add a new bookmark. Please try again later"
ADD_BOOKMARK_OK_MSG = "Bookmark added successfully"
ADD_BOOKMARK_TITLE_REQUIRED_MSG = "Error: Title is a required field"
ADD_BOOKMARK_URL_REQUIRED_MSG = "Error: URL is a required field"

DELETE_BOOKMARK_OK_MSG = "Bookmark deleted successfully"
DELETE_BOOKMARK_ERR_MSG = "Failed to delete bookmark"

IMPORT_BOOKMARKS_FILENAME = "tmp_bookmarks.html"

logger = logging.getLogger()


class App:
    def __init__(self, server, output_dir):
        self.server = server
        self.import_bookmarks_filename = Path(output_dir, IMPORT_BOOKMARKS_FILENAME)

    def display_bookmarks(self, pattern):
        """
        Args:
            pattern (str | None): a pattern to filter results

        Returns:
            display_bookmarks_section: DisplayBookmarksSection object
        """
        try:
            bookmarks = self.server.get_bookmarks(pattern)

            # clean last search
            if not pattern:
                for b in bookmarks:
                    if b.title_indexes:
                        b.title_indexes.clear()
                    if b.description_indexes:
                        b.description_indexes.clear()
                    if b.url_indexes:
                        b.url_indexes.clear()
                    if b.section_indexes:
                        b.section_indexes.clear()

            return DisplayBookmarksSection(bookmarks, None)
        except InternalException:
            return DisplayBookmarksSection(None, GET_BOOKMARKS_ERR_MSG)

    def add_bookmark(self, title, description, url, section):
        logger.info("got request to add bookmark: title=%s, desc=%s, url=%s, section=%s",
                    title, description, url, section)

        try:
            self.server.add_bookmark(title, description, url, section)
            add_bookmark_section = AddBookmarkSection("", "", "", "")
            status_section = StatusSection(True, ADD_BOOKMARK_OK_MSG)
        except InternalException:
            add_bookmark_section = AddBookmarkSection(title, description, url, section)
            status_section = StatusSection(False, ADD_BOOKMARK_ERR_MSG)
        except TitleRequiredException:
            add_bookmark_section = AddBookmarkSection(title, description, url, section)
            status_section = StatusSection(False, ADD_BOOKMARK_TITLE_REQUIRED_MSG)
        except URLRequiredException:
            add_bookmark_section = AddBookmarkSection(title, description, url, section)
            status_section = StatusSection(False, ADD_BOOKMARK_URL_REQUIRED_MSG)

        # escape add_bookmark_section
        escaped_add_bookmarks_section = AddBookmarkSection(
            html_escape(add_bookmark_section.last_title),
            html_escape(add_bookmark_section.last_description),
            html_escape(add_bookmark_section.last_url),
            html_escape(add_bookmark_section.last_section)
        )

        return status_section, self.display_bookmarks(None), escaped_add_bookmarks_section

    def delete_bookmark(self, bookmark_id):
        if self.server.delete_bookmark(bookmark_id):
            status_section = StatusSection(True, DELETE_BOOKMARK_OK_MSG)
        else:
            logger.error("failed to delete bookmark %s", bookmark_id)
            status_section = StatusSection(False, DELETE_BOOKMARK_ERR_MSG)

        return status_section, self.display_bookmarks(None)

    def import_bookmarks(self, bookmarks_file):
        """
        Returns:
            err (bool): whether an error happened
            num_added: number of bookmarks that were added
            num_failed: number of bookmarks that failed to be added
                could be because of empty title or any other error
        """
        try:
            logger.debug("import bookmarks - saving file %s to %s",
                         bookmarks_file, self.import_bookmarks_filename)
            bookmarks_file.save(self.import_bookmarks_filename)
            logger.debug("import bookmarks - file saved")
            num_added, num_failed = self.server.import_bookmarks(self.import_bookmarks_filename)
            return False, num_added, num_failed
        # pylint: disable=W0703 (broad-except)
        except Exception:
            logger.exception("failed to import bookmarks")
            return True, None, None
