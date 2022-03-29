from flask import Flask
from server import bookmarks


class App:
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        def hello_world():
            all_bookmarks = bookmarks.get_all_bookmarks()
            bookmarks_html = ""
            for b in all_bookmarks:
                bookmarks_html += f"<b>{b.title}:</b> {b.description} " \
                    f"<a href={b.link} target=\"_blank\">{b.link}</a><br>"
            return f"<h1>EasyBookmarks</h1> {bookmarks_html}"

    def run(self, host, port):
        self.app.run(host=host, port=port)
