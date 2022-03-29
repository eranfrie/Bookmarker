class Bookmark:
    def __init__(self, bookmark_id, title, description, link):
        self.id = bookmark_id
        self.title = title
        self.description = description
        self.link = link


def get_all_bookmarks():
    # TODO  hardcoded for now so we can work on the app
    bookmarks = [
        Bookmark(1, "sport", "sport 5 channel", "http://www.sport5.co.il"),
        Bookmark(2, "ynet", "news", "http://www.ynet.co.il"),
        Bookmark(3, "gmail", "mails", "http://www.gmail.com"),
    ]
    return bookmarks
