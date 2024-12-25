class DisplayBookmarksSection:
    """
    Args:
        bookmarks (list(Bookmark) | None):
            list of bookmarks to be display.
            None if error occured.
        display_bookmarks_err (str | None):
            message to be displayed in case of error
            when trying to fetch the bookmarks.
    """
    def __init__(self, bookmarks, display_bookmarks_err):
        self.bookmarks = bookmarks
        self.display_bookmarks_err = display_bookmarks_err


class BookmarkSection:
    """
    Args:
        last_title (str | ""): title to be displayed in the "add bookmark" input field.
            empty string ("") to display the placeholder.
        last_description (str | ""): description to be displayed in the "add bookmark" input field.
            empty string ("") to display the placeholder.
        last_url (str | ""): URL to be displayed in the "add bookmark" input field.
            empty string ("") to display the placeholder.
        last_section (str | ""): section to be displayed in the "add bookmark" input field.
            empty string ("") to display the placeholder.
        bookmark_id: relevant if it's an edit form, otherwise None
    """
    def __init__(self, last_title, last_description, last_url, last_section, bookmark_id):
        self.last_title = last_title
        self.last_description = last_description
        self.last_url = last_url
        self.last_section = last_section
        self.bookmark_id = bookmark_id


class StatusSection:
    def __init__(self, success, msg):
        self.success = success
        self.msg = msg
