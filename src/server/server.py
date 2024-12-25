import logging

from server.bookmark import Bookmark
from server.chrome_parser import ChromeParser
from server.server_api import InternalException, TitleRequiredException, URLRequiredException


logger = logging.getLogger()


class Server:
    def __init__(self, db):
        self.db = db
        self._cache = None

    def _invalidate_cache(self):
        logger.debug("invalidating cache")
        self._cache = None

    def _get_all_bookmarks(self):
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
            bookmarks.append(Bookmark.from_json(j))

        bookmarks.sort()
        self._cache = bookmarks
        return self._cache

    def get_bookmarks(self, patterns, is_fuzzy, include_url):
        bookmarks = self._get_all_bookmarks()
        if not patterns:
            return bookmarks

        matches = bookmarks
        patterns = [p.lower() for p in patterns]
        for p in patterns:
            matches = [m for m in matches if m.match(p, is_fuzzy, include_url)]
        return matches

    def add_bookmark(self, title, description, url, section):
        self._invalidate_cache()

        # strip input
        title = "" if title is None else title.strip()
        description = "" if description is None else description.strip()
        url = "" if url is None else url.strip()
        section = "" if section is None else section.strip()

        # input validation
        if not title:
            logger.debug("add bookmark failed - title is required")
            raise TitleRequiredException()
        if not url:
            logger.debug("add bookmark failed - url is required")
            raise URLRequiredException()

        try:
            self.db.add_bookmark(title, description, url, section)
            logger.info("bookmark added successfully")
        except Exception as e:
            logger.exception("failed to add bookmark to db: title=%s, description=%s, url=%s, section=%s",
                             title, description, url, section)
            raise InternalException() from e

    def import_bookmarks(self, filename):
        """
        Raises:
            Exception: in case of any error

        Returns:
            num_added
            num_failed
        """
        self._invalidate_cache()

        with open(filename, "r", encoding="utf-8") as f:
            html_data = f.read()

        bookmarks = ChromeParser().get_bookmarks(html_data)
        num_added = 0
        num_failed = 0
        for b in bookmarks:
            try:
                self.add_bookmark(b["title"], "", b["url"], b["section"])
                num_added += 1
            # pylint: disable=W0703 (broad-except)
            except Exception:
                logger.exception("import bookmark: failed to add bookmark: title=%s, url=%s, section=%s",
                                 b["title"], b["url"], b["section"])
                num_failed += 1

        logger.info("import bookmarks - added=%s, failed=%s", num_added, num_failed)
        return num_added, num_failed

    def get_bookmark(self, bookmark_id):
        """
        Returns:
            str if bookmark exists or None
        """
        try:
            bookmark_id = int(bookmark_id)
            j = self.db.read_bookmark(bookmark_id)
            return Bookmark.from_json(j)
        # pylint: disable=W0703 (broad-except)
        except Exception:
            logger.exception("failed to get bookmark_id %s", bookmark_id)
            return None

    def edit_bookmark(self, bookmark_id, title, description, url, section):
        self._invalidate_cache()

        # strip input
        title = "" if title is None else title.strip()
        description = "" if description is None else description.strip()
        url = "" if url is None else url.strip()
        section = "" if section is None else section.strip()

        # input validation
        if not title:
            logger.debug("edit bookmark failed - title is required")
            raise TitleRequiredException()
        if not url:
            logger.debug("edit bookmark failed - url is required")
            raise URLRequiredException()

        try:
            self.db.edit_bookmark(bookmark_id, title, description, url, section)
            logger.info("bookmark edited successfully")
        except Exception as e:
            logger.exception("failed to update bookmark in db: bookmark_id=%s, title=%s, description=%s, url=%s, section=%s",
                             bookmark_id, title, description, url, section)
            raise InternalException() from e

    def delete_bookmark(self, bookmark_id):
        """
        Returns:
            bool: whether delete succeeded or not
        """
        self._invalidate_cache()

        try:
            logger.info("requested to delete bookmark_id %s", bookmark_id)
            bookmark_id = int(bookmark_id)
            return self.db.delete_bookmark(bookmark_id)
        # pylint: disable=W0703 (broad-except)
        except Exception:
            logger.exception("failed to delete bookmark_id %s", bookmark_id)
            return False
