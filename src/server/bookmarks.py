class Bookmark:
    def __init__(self, bookmark_id, title, description, url):
        self.id = bookmark_id
        self.title = title
        self.description = description
        self.url = url


class Server:
    def __init__(self, db):
        self.db = db

    def get_all_bookmarks(self):
        """
        Returns:
            list of Bookmark objects
        """
        bookmarks = []
        bookmarks_json = self.db.read_all_bookmarks()
        for j in bookmarks_json:
            bookmarks.append(
                Bookmark(
                    j["id"],
                    j["title"],
                    j["description"],
                    j["url"],
                )
            )
        return bookmarks

    def add_bookmark(self, title, description, url):
        self.db.add_bookmark(title, description, url)
