from pathlib import Path
import logging

from utils.html_utils import html_escape
from server.server_api import InternalException, TitleRequiredException, URLRequiredException
from app.app_sections import DisplayBookmarksSection, BookmarkSection, StatusSection


GET_BOOKMARKS_ERR_MSG = "Internal error. Please try again later"
ADD_BOOKMARK_ERR_MSG = "Internal error: Failed to add a new bookmark. Please try again later"
ADD_BOOKMARK_OK_MSG = "Bookmark added successfully"
BOOKMARK_TITLE_REQUIRED_MSG = "Error: Title is a required field"
BOOKMARK_URL_REQUIRED_MSG = "Error: URL is a required field"
EDIT_BOOKMARK_ERR_MSG = "Internal error: Failed to edit a bookmark. Please try again later"
EDIT_BOOKMARK_OK_MSG = "Bookmark edited successfully"

DELETE_BOOKMARK_OK_MSG = "Bookmark deleted successfully"
DELETE_BOOKMARK_ERR_MSG = "Failed to delete bookmark"

IMPORT_BOOKMARKS_FILENAME = "tmp_bookmarks.html"

logger = logging.getLogger()


class App:
    def __init__(self, server, output_dir):
        self.server = server
        self.import_bookmarks_filename = Path(output_dir, IMPORT_BOOKMARKS_FILENAME)

    def display_bookmarks(self, patterns, is_fuzzy, include_url, favorites_only):
        """
        Args:
            patterns (list<str> | None): patterns to filter results
            is_fuzzy (bool): whether to perform a fuzzy search or regular search
            include_url (bool): whether to filter by URL too
            favorites_only (bool): whether to filter favorited bookmarks

        Returns:
            display_bookmarks_section: DisplayBookmarksSection object
        """
        try:
            bookmarks = self.server.get_bookmarks(patterns, is_fuzzy, include_url, favorites_only)
            return DisplayBookmarksSection(bookmarks, None)
        except InternalException:
            return DisplayBookmarksSection(None, GET_BOOKMARKS_ERR_MSG)

    def add_bookmark(self, title, description, url, section):
        logger.info("got request to add bookmark: title=%s, desc=%s, url=%s, section=%s",
                    title, description, url, section)

        try:
            self.server.add_bookmark(title, description, url, section)
            bookmark_section = BookmarkSection("", "", "", "", None)
            status_section = StatusSection(True, ADD_BOOKMARK_OK_MSG)
        except InternalException:
            bookmark_section = BookmarkSection(title, description, url, section, None)
            status_section = StatusSection(False, ADD_BOOKMARK_ERR_MSG)
        except TitleRequiredException:
            bookmark_section = BookmarkSection(title, description, url, section, None)
            status_section = StatusSection(False, BOOKMARK_TITLE_REQUIRED_MSG)
        except URLRequiredException:
            bookmark_section = BookmarkSection(title, description, url, section, None)
            status_section = StatusSection(False, BOOKMARK_URL_REQUIRED_MSG)

        # escape bookmark_section
        escaped_bookmarks_section = BookmarkSection(
            html_escape(bookmark_section.last_title),
            html_escape(bookmark_section.last_description),
            html_escape(bookmark_section.last_url),
            html_escape(bookmark_section.last_section),
            None
        )

        return status_section, self.display_bookmarks(None, None, None, None), escaped_bookmarks_section

    def edit_bookmark_form(self, bookmark_id):
        return self.server.get_bookmark(bookmark_id)

    def edit_bookmark(self, bookmark_id, title, description, url, section):
        logger.info("got request to edit bookmark: bookmark_id=%s, title=%s, description=%s, url=%s, section=%s",
                    bookmark_id, title, description, url, section)

        try:
            self.server.edit_bookmark(bookmark_id, title, description, url, section)
            bookmark_section = BookmarkSection("", "", "", "", None)
            status_section = StatusSection(True, EDIT_BOOKMARK_OK_MSG)
        except InternalException:
            bookmark_section = BookmarkSection(title, description, url, section, None)
            status_section = StatusSection(False, EDIT_BOOKMARK_ERR_MSG)
            return status_section, None, None
        except TitleRequiredException:
            bookmark_section = BookmarkSection(title, description, url, section, None)
            status_section = StatusSection(False, BOOKMARK_TITLE_REQUIRED_MSG)
            return status_section, None, None
        except URLRequiredException:
            bookmark_section = BookmarkSection(title, description, url, section, None)
            status_section = StatusSection(False, BOOKMARK_URL_REQUIRED_MSG)
            return status_section, None, None

        # escape bookmark_section
        escaped_bookmark_section = BookmarkSection(
            html_escape(bookmark_section.last_title),
            html_escape(bookmark_section.last_description),
            html_escape(bookmark_section.last_url),
            html_escape(bookmark_section.last_section),
            None
        )

        return status_section, self.display_bookmarks(None, None, None, None), escaped_bookmark_section

    def toggle_favorited(self, bookmark_id):
        return self.server.toggle_favorited(bookmark_id)

    def delete_bookmark(self, bookmark_id):
        if self.server.delete_bookmark(bookmark_id):
            status_section = StatusSection(True, DELETE_BOOKMARK_OK_MSG)
        else:
            logger.error("failed to delete bookmark %s", bookmark_id)
            status_section = StatusSection(False, DELETE_BOOKMARK_ERR_MSG)

        return status_section, self.display_bookmarks(None, None, None, None)

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
