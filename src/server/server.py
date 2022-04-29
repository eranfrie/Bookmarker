import logging

from server.chrome_parser import ChromeParser
from server.server_api import InternalException, TitleRequiredException, URLRequiredException


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

        # strip input
        title = title if title is None else title.strip()
        description = description if description is None else description.strip()
        url = url if url is None else url.strip()

        # input validation
        if not title:
            logger.debug("add bookmark failed - title is required")
            raise TitleRequiredException()
        if not url:
            logger.debug("add bookmark failed - url is required")
            raise URLRequiredException()

        try:
            self.db.add_bookmark(title, description, url)
            logger.info("bookmark added successfully")
        except Exception as e:
            logger.exception("failed to add bookmark to db: title=%s, description=%s, url=%s",
                             title, description, url)
            raise InternalException() from e

    def import_bookmarks(self, filename):
        """
        Raises:
            Exception: in case of any error
        """
        self._invalidate_cache()

        with open(filename, "r", encoding="utf-8") as f:
            html_data = f.read()

        bookmarks = ChromeParser().get_bookmarks(html_data)
        for b in bookmarks:
            try:
                self.add_bookmark(b["title"], "", b["url"])
            # pylint: disable=W0703 (broad-except)
            except Exception:
                logger.warning("import bookmark: failed to add bookmark: title=%s, description=%s, url=%s",
                               b["title"], b["description"], b["url"])
