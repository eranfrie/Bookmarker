from flask import Flask


class App:
    def __init__(self, server):
        self.server = server
        self.app = Flask(__name__)

        @self.app.route('/')
        def hello_world():
            all_bookmarks = self.server.get_all_bookmarks()
            bookmarks_html = ""
            for b in all_bookmarks:
                bookmarks_html += f"<b>{b.title}:</b> {b.description} " \
                    f"<a href={b.url} target=\"_blank\">{b.url}</a><br>"
            return f"<h1>EasyBookmarks</h1> {bookmarks_html}"

    def run(self, host, port):
        self.app.run(host=host, port=port)
