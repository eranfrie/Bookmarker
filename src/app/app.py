import logging

from server.server_api import InternalException
from server.bookmarks import html_escape


GET_BOOKMARKS_ERR_MSG = "Internal error. Please try again later"
ADD_BOOKMARK_ERR_MSG = "Internal error: Failed to add a new bookmark. Please try again later"
ADD_BOOKMARK_OK_MSG = "Bookmark added successfully"
ADD_BOOKMARK_TITLE_REQUIRED_MSG = "Error: Title is a required field"
ADD_BOOKMARK_URL_REQUIRED_MSG = "Error: URL is a required field"

logger = logging.getLogger()


class App:
    def __init__(self, server):
        self.server = server

    def _main_page(
            self,
            add_bookmark_succeeded,
            add_bookmark_msg,
            add_title_val,
            add_description_val,
            add_url_val):
        """Returns all information to be displayed in the main page.

        Args:
            add_bookmark_succeeded (bool):
                True/False if adding a bookmark is being requested and succeeded/failed accordingly.
                None if adding a bookmark is not being requested.
            add_bookmark_msg (str | None):
                if add_bookmark_succeeded is True/False, a message to display.
            add_title_val (str | ""): title to be displayed in the "add bookmark" inut field.
                empty string ("") to display the placeholder.
            add_description_val (str | ""): description to be displayed in the "add bookmark" inut field.
                empty string ("") to display the placeholder.
            add_url_val (str | ""): URL to be displayed in the "add bookmark" inut field.
                empty string ("") to display the placeholder.

        Returns:
            returns the parameters as is
            bookmarks (list(Bookmark) | None):
                list of bookmarks to be display.
                None if error occured.
            get_bookmarks_err (str): message to be displayed in case of error
                when trying to fetch the bookmarks.
        """
        # bookmarks section
        bookmarks = None
        get_bookmarks_err = None
        try:
            bookmarks = self.server.get_all_bookmarks()
        except InternalException:
            get_bookmarks_err = GET_BOOKMARKS_ERR_MSG

        return \
            add_bookmark_succeeded, \
            add_bookmark_msg, \
            html_escape(add_title_val), \
            html_escape(add_description_val), \
            html_escape(add_url_val), \
            bookmarks, \
            get_bookmarks_err

    def get_bookmarks(self):
        """
        Returns all information needed to display the main page
        (see `_main_page` function).
        """
        return self._main_page(None, None, "", "", "")

    def add_bookmark(self, title, description, url):
        """
        Returns all information needed to display the main page
        (see `_main_page` function).
        """
        logger.info("got request to add bookmark: title=%s, desc=%s, url=%s",
                    title, description, url)

        # input validation
        # not expected to happen because browser enforces it (using HTML 'required' attribute)
        if not title or not url:
            add_bookmark_msg = ADD_BOOKMARK_TITLE_REQUIRED_MSG if not title \
                    else ADD_BOOKMARK_URL_REQUIRED_MSG
            return self._main_page(
                    False, add_bookmark_msg,
                    title, description, url)

        try:
            self.server.add_bookmark(title, description, url)
            return self._main_page(
                    True, ADD_BOOKMARK_OK_MSG,
                    "", "", "")
        except InternalException:
            return self._main_page(
                    False, ADD_BOOKMARK_ERR_MSG,
                    title, description, url)
