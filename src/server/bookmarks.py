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
        self._cache = None

    def _invalidate_cache(self):
        logger.debug("invalidating cache")
        self._cache = None

    def get_all_bookmarks(self):
        """
        Returns:
            list of Bookmark objects
        """
        # don't use cache if cache is None -
        #     it means either cache was invalidated or an error occurred in previous call
        #     if an error occurred in previous call - we want to try again this time
        # or if cache size is 0 -
        #     mainly for tests (and it's not an interesting case to cache)
        if self._cache:
            return self._cache

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

        self._cache = bookmarks
        return bookmarks

    def add_bookmark(self, title, description, url):
        self._invalidate_cache()

        try:
            self.db.add_bookmark(title, description, url)
            logger.info("bookmark added successfully")
        except Exception as e:
            logger.exception("failed to add bookmark to db: title=%s, description=%s, url=%s",
                             title, description, url)
            raise InternalException() from e
