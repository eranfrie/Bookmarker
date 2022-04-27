import logging

from server.server_api import InternalException


logger = logging.getLogger()


class Bookmark:
    def __init__(self, bookmark_id, title, description, url):
        self.id = bookmark_id
        self.title = title
        self.description = description
        self.url = url


class Server:
    def __init__(self, db):
        self.db = db

    def get_all_bookmarks(self):
        """
        Returns:
            list of Bookmark objects
        """
        bookmarks = []

        try:
            bookmarks_json = self.db.read_all_bookmarks()
        except Exception as e:
            logger.exception("failed to read bookmarks from db")
            raise InternalException() from e

        for j in bookmarks_json:
            bookmarks.append(
                Bookmark(
                    j["id"],
                    j["title"],
                    j["description"],
                    j["url"],
                )
            )
        return bookmarks

    def add_bookmark(self, title, description, url):
        try:
            self.db.add_bookmark(title, description, url)
            logger.info("bookmark added successfully")
        except Exception as e:
            logger.exception("failed to add bookmark to db: title=%s, description=%s, url=%s",
                             title, description, url)
            raise InternalException() from e
