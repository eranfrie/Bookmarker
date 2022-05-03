from pathlib import Path
import logging

from flask import escape

from server.server_api import InternalException, TitleRequiredException, URLRequiredException
from server.bookmark import Bookmark
from app.app_sections import DisplayBookmarksSection, AddBookmarkSection


GET_BOOKMARKS_ERR_MSG = "Internal error. Please try again later"
ADD_BOOKMARK_ERR_MSG = "Internal error: Failed to add a new bookmark. Please try again later"
ADD_BOOKMARK_OK_MSG = "Bookmark added successfully"
ADD_BOOKMARK_TITLE_REQUIRED_MSG = "Error: Title is a required field"
ADD_BOOKMARK_URL_REQUIRED_MSG = "Error: URL is a required field"

IMPORT_BOOKMARKS_FILENAME = "tmp_bookmarks.html"

logger = logging.getLogger()


def html_escape(text):
    if not text:
        return text
    return escape(text)


class App:
    def __init__(self, server, output_dir):
        self.server = server
        self.import_bookmarks_filename = Path(output_dir, IMPORT_BOOKMARKS_FILENAME)

    def _main_page(self, add_bookmarks_section):
        """Returns all information to be displayed in the main page.

        Args:
            add_bookmarks_section: DisplayBookmarksSection object

        Returns:
            escaped_display_bookmarks_section:
                DisplayBookmarksSection object after escaping the relevant fields
            escaped_add_bookmarks_section:
                AddBookmarkSection object after escaping the relevant fields
        """
        try:
            escaped_bookmarks = []
            for b in self.server.get_all_bookmarks():
                escaped_bookmarks.append(
                    Bookmark(
                        b.id,
                        html_escape(b.title),
                        html_escape(b.description),
                        html_escape(b.url),
                        html_escape(b.section)
                    )
                )

            escaped_display_bookmarks_section = DisplayBookmarksSection(escaped_bookmarks, None)
        except InternalException:
            escaped_display_bookmarks_section = DisplayBookmarksSection(None, GET_BOOKMARKS_ERR_MSG)

        # escape add_bookmarks_section
        escaped_add_bookmarks_section = AddBookmarkSection(
            add_bookmarks_section.last_op_succeeded,
            add_bookmarks_section.last_op_msg,
            html_escape(add_bookmarks_section.last_title),
            html_escape(add_bookmarks_section.last_description),
            html_escape(add_bookmarks_section.last_url),
            html_escape(add_bookmarks_section.last_section)
        )

        return escaped_display_bookmarks_section, escaped_add_bookmarks_section

    def display_bookmarks(self):
        """
        Returns all information needed to display the main page
        (see `_main_page` function).
        """
        add_bookmarks_section = AddBookmarkSection(None, None, "", "", "", "")
        return self._main_page(add_bookmarks_section)

    def add_bookmark(self, title, description, url, section):
        """
        Returns all information needed to display the main page
        (see `_main_page` function).
        """
        logger.info("got request to add bookmark: title=%s, desc=%s, url=%s, section=%s",
                    title, description, url, section)

        try:
            self.server.add_bookmark(title, description, url, section)
            add_bookmarks_section = AddBookmarkSection(True, ADD_BOOKMARK_OK_MSG, "", "", "", "")
            return self._main_page(add_bookmarks_section)
        except InternalException:
            add_bookmarks_section = AddBookmarkSection(
                    False, ADD_BOOKMARK_ERR_MSG, title, description, url, section)
            return self._main_page(add_bookmarks_section)
        except TitleRequiredException:
            add_bookmarks_section = AddBookmarkSection(
                    False, ADD_BOOKMARK_TITLE_REQUIRED_MSG, title, description, url, section)
            return self._main_page(add_bookmarks_section)
        except URLRequiredException:
            add_bookmarks_section = AddBookmarkSection(
                    False, ADD_BOOKMARK_URL_REQUIRED_MSG, title, description, url, section)
            return self._main_page(add_bookmarks_section)

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
