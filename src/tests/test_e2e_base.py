from multiprocessing import Process
from pathlib import Path
from time import sleep

import requests

from main import main
from data import sqlite
from data.sqlite import Sqlite


OUTPUT_DIR = "tmp"
DB_FILENAME = "bookmarks.db"


# pylint: disable=W0201, R0201
class TestE2eBase:
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

    def _compare_num_bookmarks(self, response, expected_num_bookmarks, db_avail=True):
        assert response.status_code == 200
        assert response.text.count("href") == expected_num_bookmarks
        if db_avail:
            assert f"Total: {expected_num_bookmarks}" in response.text
            assert self._count_bookmarks_in_db() == expected_num_bookmarks

    def _add_bookmark_to_db(self, title, description, url):
        db_filename = Path(OUTPUT_DIR, DB_FILENAME)
        db = Sqlite(db_filename)
        db.add_bookmark(title, description, url)

    def _count_bookmarks_in_db(self):
        db_filename = Path(OUTPUT_DIR, DB_FILENAME)
        db = Sqlite(db_filename)
        conn, cursor = db._connect()  # pylint: disable=W0212
        res = cursor.execute(f"SELECT COUNT() FROM {sqlite.BOOKMARKS_TABLE};")
        res = res.fetchone()[0]
        Sqlite._close(conn)  # pylint: disable=W0212
        return res

    def _delete_db(self):
        try:
            Path(OUTPUT_DIR, DB_FILENAME).unlink()
        except FileNotFoundError:
            pass
