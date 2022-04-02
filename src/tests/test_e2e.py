from multiprocessing import Process
from time import sleep
from pathlib import Path

import requests

from main import main


URL = "http://localhost:8000"
DB_FILENAME = "bookmarks.db"


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
