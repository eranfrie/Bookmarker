from multiprocessing import Process
from time import sleep
from pathlib import Path

import requests

from main import main


DB_FILENAME = "bookmarks.db"

URL = "http://localhost:8000"
ADD_BOOKMARK_URL = f"{URL}/add_bookmark"


# pylint: disable=W0201, R0201
class TestE2e:
    def setup(self):
        # delete old db
        try:
            Path("tmp", DB_FILENAME).unlink()
        except FileNotFoundError:
            pass

        # start the server
        override_config = {
            "output_dir": "tmp",
            "console_log_level": "WARNING",
        }
        self.server = Process(target=main, args=(override_config,))
        self.server.start()
        # wait for server to start
        for _ in range(3):
            try:
                r = requests.get("http://localhost:8000")
                if r.status_code == 200:
                    return
            except requests.exceptions.ConnectionError:
                pass

            sleep(2)

        self.teardown()
        raise Exception("Server failed to start")

    def teardown(self):
        self.server.terminate()
        self.server.join()

    def _compare_num_bookmarks(self, response, expected_num_bookmarks):
        assert response.status_code == 200
        assert response.text.count("href") == expected_num_bookmarks

    def test_empty_get(self):
        response = requests.get(URL)
        self._compare_num_bookmarks(response, 0)

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
