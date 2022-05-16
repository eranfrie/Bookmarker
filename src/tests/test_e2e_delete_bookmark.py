import requests

from app import app
from tests.test_e2e_base import TestE2eBase, URL


class TestE2eDeleteBookmark(TestE2eBase):
    def test_delete_bookmark_success(self):
        self._add_bookmark_to_db("test_title", "test_description",
                                 "http://www.test.com", "test_section")
        assert self._count_bookmarks_in_db() == 1

        bookmark_id = 1
        payload = {"bookmark_id": bookmark_id}
        response = requests.post(URL.DELETE_BOOKMARK.value, data=payload)
        self._compare_num_bookmarks(response, 0)
        assert self._count_bookmarks_in_db() == 0
        assert response.text.count(app.DELETE_BOOKMARK_OK_MSG) == 1

    def test_delete_2_bookmarks_success(self):
        for _ in range(5):
            self._add_bookmark_to_db("test_title", "test_description",
                                     "http://www.test.com", "test_section")
        assert self._count_bookmarks_in_db() == 5

        bookmark_id = 2
        payload = {"bookmark_id": bookmark_id}
        response = requests.post(URL.DELETE_BOOKMARK.value, data=payload)
        self._compare_num_bookmarks(response, 4)
        assert self._count_bookmarks_in_db() == 4
        assert response.text.count(app.DELETE_BOOKMARK_OK_MSG) == 1

        bookmark_id = 4
        payload = {"bookmark_id": bookmark_id}
        response = requests.post(URL.DELETE_BOOKMARK.value, data=payload)
        self._compare_num_bookmarks(response, 3)
        assert self._count_bookmarks_in_db() == 3
        assert response.text.count(app.DELETE_BOOKMARK_OK_MSG) == 1

    def test_delete_bookmark_fail(self):
        self._add_bookmark_to_db("test_title", "test_description",
                                 "http://www.test.com", "test_section")
        assert self._count_bookmarks_in_db() == 1

        bookmark_id = 1234
        payload = {"bookmark_id": bookmark_id}
        response = requests.post(URL.DELETE_BOOKMARK.value, data=payload)
        self._compare_num_bookmarks(response, 1)
        assert self._count_bookmarks_in_db() == 1
        assert response.text.count(app.DELETE_BOOKMARK_ERR_MSG) == 1

    def test_delete_bookmark_fail_no_db(self):
        # delete the db in order to get an internal error.
        self._delete_db()

        bookmark_id = 1
        payload = {"bookmark_id": bookmark_id}
        response = requests.post(URL.DELETE_BOOKMARK.value, data=payload)
        self._compare_num_bookmarks(response, 0, db_avail=False)
        assert response.text.count(app.DELETE_BOOKMARK_ERR_MSG) == 1
        assert response.text.count(app.GET_BOOKMARKS_ERR_MSG) == 1
