from multiprocessing import Process
from time import sleep
from pathlib import Path
import re

import requests

from main import main
from data.sqlite import Sqlite
from app import app


OUTPUT_DIR = "tmp"
DB_FILENAME = "bookmarks.db"

URL = "http://localhost:8000"
ADD_BOOKMARK_URL = f"{URL}/add_bookmark"


# pylint: disable=W0201, R0201
class TestE2e:
    def setup(self):
        # delete old db
        self._delete_db()

        # start the server
        override_config = {
            "output_dir": OUTPUT_DIR,
            "console_log_level": "WARNING",
        }
        self.server = Process(target=main, args=(override_config,))
        self.server.start()
        # wait for server to start
        for _ in range(120):
            try:
                r = requests.get("http://localhost:8000")
                if r.status_code == 200:
                    return
            except requests.exceptions.ConnectionError:
                pass

            sleep(0.05)

        self.teardown()
        raise Exception("Server failed to start")

    def teardown(self):
        self.server.terminate()
        self.server.join()

    def _compare_num_bookmarks(self, response, expected_num_bookmarks, check_total=True):
        assert response.status_code == 200
        assert response.text.count("href") == expected_num_bookmarks
        if check_total:
            assert f"Total: {expected_num_bookmarks}" in response.text

    def _add_bookmark_to_db(self, title, description, url):
        db_filename = Path(OUTPUT_DIR, DB_FILENAME)
        db = Sqlite(db_filename)
        db.add_bookmark(title, description, url)

    def _delete_db(self):
        try:
            Path(OUTPUT_DIR, DB_FILENAME).unlink()
        except FileNotFoundError:
            pass

    def test_empty_get(self):
        response = requests.get(URL)
        self._compare_num_bookmarks(response, 0)

    def test_get_bookmarks(self):
        response = requests.get(URL)
        self._compare_num_bookmarks(response, 0)

        self._add_bookmark_to_db("test_title_1", "test_description_1", "http://www.test_1.com")
        response = requests.get(URL)
        self._compare_num_bookmarks(response, 1)

        self._add_bookmark_to_db("test_title_2", "test_description_2", "http://www.test_2.com")
        response = requests.get(URL)
        self._compare_num_bookmarks(response, 2)

    def test_get_internal_err(self):
        # delete the db in order to get an internal error.
        self._delete_db()

        response = requests.get(URL)
        self._compare_num_bookmarks(response, 0, check_total=False)
        assert response.text.count(app.GET_BOOKMARKS_ERR_MSG) == 1

    def test_add_bookmark(self):
        # add a bookmark
        payload = {
            "title": "test_title",
            "description": "test_description",
            "url": "http://www.test.com",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 1)

        # add another bookmark
        payload = {
            "title": "test_title_2",
            "description": "test_description_2",
            "url": "http://www.test_2.com",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 2)

        # validate fields order
        pattern = "test_title.*test_description.*http://www\\.test\\.com.*" \
                  "test_title_2.*test_description_2.*http://www\\.test_2\\.com"
        assert re.search(pattern, response.text)

    def test_add_bookmark_with_missing_description(self):
        """
        description is optional field - adding a bookmark should succeed.
        """
        payload = {
            "title": "test_title",
            "url": "http://www.test.com",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 1)

    def test_not_desplaying_missing_description(self):
        """
        a missing (optional) description should not be displayed as "None".
        """
        payload = {
            "title": "test_title",
            "url": "http://www.test.com",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 1)
        assert "None" not in response.text

    def test_add_bookmark_internal_err(self):
        # delete the db in order to get an internal error.
        self._delete_db()

        payload = {
            "title": "test_title",
            "description": "test_description",
            "url": "http://www.test.com",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 0, check_total=False)
        assert response.text.count(app.ADD_BOOKMARK_ERR_MSG) == 1
        assert response.text.count(app.GET_BOOKMARKS_ERR_MSG) == 1

        response = requests.get(URL)
        self._compare_num_bookmarks(response, 0, check_total=False)
        assert response.text.count(app.ADD_BOOKMARK_ERR_MSG) == 0
        assert response.text.count(app.GET_BOOKMARKS_ERR_MSG) == 1

    def test_add_bookmark_success_msg(self):
        # add a bookmark
        payload = {
            "title": "test_title",
            "description": "test_description",
            "url": "http://www.test.com",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 1)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 1

        response = requests.get(URL)
        self._compare_num_bookmarks(response, 1)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 0

        # add another bookmark
        payload = {
            "title": "test_title_2",
            "description": "test_description_2",
            "url": "http://www.test_2.com",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 2)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 1

        response = requests.get(URL)
        self._compare_num_bookmarks(response, 2)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 0

    def test_add_bookmark_title_required(self):
        payload = {
            "description": "test_description",
            "url": "http://www.test.com",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 0)
        assert response.text.count(app.ADD_BOOKMARK_TITLE_REQUIRED_MSG) == 1

    def test_add_bookmark_url_required(self):
        payload = {
            "title": "test_title_2",
            "description": "test_description",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 0)
        assert response.text.count(app.ADD_BOOKMARK_URL_REQUIRED_MSG) == 1

    def test_html_escape(self):
        payload = {
            "title": "<>test_title",
            "description": "<>test_description",
            "url": "<>http://www.test.com",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 1)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 1
        pattern = "&lt;&gt;test_title.*&lt;&gt;test_description.*&lt;&gt;http://www\\.test\\.com"
        assert re.search(pattern, response.text)
