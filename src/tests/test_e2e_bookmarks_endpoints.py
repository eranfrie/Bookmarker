import requests

from app import app
from tests.test_e2e_base import TestE2eBase, URL


# disable similar code check
# pylint: disable=R0801
class TestE2eBookmarksEndpoint(TestE2eBase):
    def _compare_num_bookmarks(self, response, expected_num_bookmarks, db_avail=True):
        assert response.status_code == 200
        assert response.text.count("href") == \
            expected_num_bookmarks + response.text.count("font-awesome.min.css")
        if db_avail:
            assert f"Total: {expected_num_bookmarks}" in response.text
            assert self._count_bookmarks_in_db() == expected_num_bookmarks

    def test_empty(self):
        response = requests.get(URL.BOOKMARKS.value)
        self._compare_num_bookmarks(response, 0)
        # test that where there are 0 bookmarks,
        # we don't accidentally display the error msg
        assert app.GET_BOOKMARKS_ERR_MSG not in response.text

    def test_get_one_bookmark(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "http://www.test_1.com", "test_section_1")
        response = requests.get(URL.BOOKMARKS.value)
        self._compare_num_bookmarks(response, 1)

    def test_get_two_bookmark(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "http://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "http://www.test_2.com", "test_section_2")
        response = requests.get(URL.BOOKMARKS.value)
        self._compare_num_bookmarks(response, 2)

    def test_get_internal_err(self):
        # delete the db in order to get an internal error.
        self._delete_db()

        response = requests.get(URL.BOOKMARKS.value)
        self._compare_num_bookmarks(response, 0, db_avail=False)
        assert response.text.count(app.GET_BOOKMARKS_ERR_MSG) == 1

    def test_search_no_results(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.BOOKMARKS.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "test_title_3"
        response = requests.get(URL.BOOKMARKS.value, params={"pattern": pattern})
        self._compare_num_bookmarks(response, 0, db_avail=False)
        assert response.text.count("mark>") == 0

    def test_search_one_results(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.BOOKMARKS.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "test_title_1"
        response = requests.get(URL.BOOKMARKS.value, params={"pattern": pattern})
        self._compare_num_bookmarks(response, 1, db_avail=False)
        assert response.text.count("mark>") == len(pattern) * 2
