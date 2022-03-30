import logging
import sqlite3


logger = logging.getLogger()

BOOKMARKS_TABLE = "bookmarks"


class Sqlite:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        logger.info("DB filename = %s", self.db_filename)

        self._create_tables_if_not_exists()

    def _connect(self):
        conn = sqlite3.connect(self.db_filename)
        return conn, conn.cursor()

    @classmethod
    def _close(cls, conn):
        conn.commit()
        conn.close()

    def _create_tables_if_not_exists(self):
        conn, cursor = self._connect()
        bookmarks_table = \
            f"CREATE TABLE IF NOT EXISTS {BOOKMARKS_TABLE} (" \
            "id integer PRIMARY KEY," \
            "title text NOT NULL," \
            "description text," \
            "url text NOT NULL" \
            ");"
        cursor.execute(bookmarks_table)
        Sqlite._close(conn)

    def read_all_bookmarks(self):
        """
        Returns:
            list of dict (each dict is a record from the db)
        """
        conn, cursor = self._connect()
        bookmarks = []
        records = cursor.execute(f"SELECT * FROM {BOOKMARKS_TABLE};")
        for record in records:
            bookmarks.append(
                {
                    "id": record[0],
                    "title": record[1],
                    "description": record[2],
                    "url": record[3],
                }
            )
        Sqlite._close(conn)
        return bookmarks
