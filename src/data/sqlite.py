import logging
import sqlite3


logger = logging.getLogger()

BOOKMARKS_TABLE = "bookmarks"


def sql_escape(text):
    if not text:
        return text
    return text.replace("'", "''")


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
        description (optional field) should be None if missing from the db.

        Returns:
            list of dict (each dict is a record from the db)
        """
        conn, cursor = self._connect()
        bookmarks = []

        try:
            records = cursor.execute(f"SELECT * FROM {BOOKMARKS_TABLE};")
        except Exception as e:
            Sqlite._close(conn)
            raise e

        for record in records:
            # check if description is not empty and not None
            # (in sqlite, missing field is returned as "None" string)
            description = None
            if record[2] and record[2] != "None":
                description = record[2]

            bookmarks.append(
                {
                    "id": record[0],
                    "title": record[1],
                    "description": description,
                    "url": record[3],
                }
            )
        Sqlite._close(conn)
        return bookmarks

    def add_bookmark(self, title, description, url):
        conn, cursor = self._connect()
        try:
            cursor.execute(f"INSERT INTO {BOOKMARKS_TABLE} (title, description, url) "
                           f"VALUES ('{sql_escape(title)}', "
                           f"'{sql_escape(description)}', "
                           f"'{sql_escape(url)}');")
        finally:
            Sqlite._close(conn)
