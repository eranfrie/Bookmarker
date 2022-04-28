import requests

from tests.test_e2e_base import TestE2eBase, URL


# pylint: disable=R0201 (no-self-use)
class TestE2eCaching(TestE2eBase):
    def test_cache(self):
        # add a bookmark
        response = self._add_bookmark("test_title", "test_description", "http://www.test.com")
        self._compare_num_bookmarks(response, 1)

        # add a bookmark directly to the DB
        # but still get one bookmark (cached)
        self._add_bookmark_to_db("test_title", "test_description", "http://www.test.com")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 1, db_avail=False)

    def test_invalidate_cache(self):
        # add a bookmark directly to DB
        self.test_cache()

        # add a bookmark via API - cache should be invalidated
        response = self._add_bookmark("test_title", "test_description", "http://www.test.com")
        self._compare_num_bookmarks(response, 3)

    def test_cache_delted_db(self):
        response = self._add_bookmark("test_title", "test_description", "http://www.test.com")
        self._compare_num_bookmarks(response, 1)

        self._delete_db()

        # should get cached bookmarks
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 1, db_avail=False)

    def test_empty_db_no_cache(self):
        # get 0 bookmarks
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 0)

        # making sure cache is not used after getting 0 bookmarks
        # by adding a bookmark directly to Db and sending GET again
        self._add_bookmark_to_db("test_title", "test_description", "http://www.test.com")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 1)
