import logging
import sqlite3


logger = logging.getLogger()

BOOKMARKS_TABLE = "bookmarks"


def sql_escape(text):
    if not text:
        return text
    return text.replace("'", "''")


def record_to_json(record):
    # check if description is not empty and not None
    # (in sqlite, missing field is returned as "None" string)
    description = None
    if record[2] and record[2] != "None":
        description = record[2]

    return {
        "id": record[0],
        "title": record[1],
        "description": description,
        "url": record[3],
        "section": record[4],
        "is_favorited": bool(record[5]),
    }


class Sqlite:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        logger.info("DB filename = %s", self.db_filename)

        self._create_tables_if_not_exists()
        self._migrate_bookmarks_table()

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
            "url text NOT NULL," \
            "section text," \
            "is_favorited BOOLEAN NOT NULL" \
            ");"
        cursor.execute(bookmarks_table)
        Sqlite._close(conn)

    def _migrate_bookmarks_table(self):
        """Migrate the bookmarks tabke if needed.

        A 'is_favorited' column was added. This function checks
        if it's missing, creates it with 'false' values.
        """
        if self._does_column_exist("is_favorited"):
            return

        logger.info("'is_favorited' is missing - creating it")

        conn, cursor = self._connect()
        cursor.execute(f"ALTER TABLE {BOOKMARKS_TABLE} ADD COLUMN is_favorited BOOLEAN")
        cursor.execute(f"UPDATE {BOOKMARKS_TABLE} SET is_favorited=False;");
        Sqlite._close(conn)

    def _does_column_exist(self, column_name):
        conn, cursor = self._connect()

        column_exists = False

        cursor.execute(f"PRAGMA table_info({BOOKMARKS_TABLE})")
        columns = cursor.fetchall()
        for column in columns:
            if column[1] == column_name:
                column_exists = True
                break

        Sqlite._close(conn)
        return column_exists

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
            bookmarks.append(record_to_json(record))

        Sqlite._close(conn)
        return bookmarks

    def read_bookmark(self, bookmark_id):
        """
        Returns:
            dict: a record from the db
        """
        conn, cursor = self._connect()

        try:
            records = cursor.execute(f"SELECT * FROM {BOOKMARKS_TABLE} where id={bookmark_id};")
        except Exception as e:
            Sqlite._close(conn)
            raise e

        bookmark = None
        for record in records:  # only one record will be found
            bookmark = record_to_json(record)
        Sqlite._close(conn)
        return bookmark

    def add_bookmark(self, title, description, url, section, is_favorited):
        conn, cursor = self._connect()
        try:
            cursor.execute(f"INSERT INTO {BOOKMARKS_TABLE} (title, description, url, section, is_favorited) "
                           f"VALUES ('{sql_escape(title)}', "
                           f"'{sql_escape(description)}', "
                           f"'{sql_escape(url)}', "
                           f"'{sql_escape(section)}', "
                           f"{is_favorited});")
        finally:
            Sqlite._close(conn)

    def edit_bookmark(self, bookmark_id, title, description, url, section):
        conn, cursor = self._connect()
        try:
            cursor.execute(f"UPDATE {BOOKMARKS_TABLE} "
                           f"SET title='{sql_escape(title)}', "
                           f"description='{sql_escape(description)}', "
                           f"url='{sql_escape(url)}', "
                           f"section='{sql_escape(section)}' "
                           f"WHERE id={bookmark_id};")
        finally:
            Sqlite._close(conn)

    def toggle_favorited(self, bookmark_id):
        bookmark = self.read_bookmark(bookmark_id)

        was_favorited = bookmark["is_favorited"]
        new_state = not was_favorited

        conn, cursor = self._connect()
        try:
            cursor.execute(f"UPDATE {BOOKMARKS_TABLE} "
                           f"SET "
                           f"is_favorited={new_state} "
                           f"WHERE id={bookmark_id};")
            return new_state
        except Exception:
            return not new_state
        finally:
            Sqlite._close(conn)

    def delete_bookmark(self, bookmark_id):
        """
        Args:
            bookmark_id (int): no need to escapse
        """
        rows_deleted = 0
        conn, cursor = self._connect()
        try:
            cursor.execute(f"DELETE FROM {BOOKMARKS_TABLE} WHERE id=?;", (bookmark_id, ))
            rows_deleted = cursor.rowcount
        finally:
            Sqlite._close(conn)
        return rows_deleted == 1
