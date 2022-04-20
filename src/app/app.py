import logging

from flask import Flask, request


logger = logging.getLogger()


class App:
    def __init__(self, server):
        self.server = server
        self.app = Flask(__name__)

        def main_page_html():
            html = "<h1>EasyBookmarks</h1>"

            # add bookmark form
            html += '<h4>Add a new bookmark</h4>' \
                '<form action="/add_bookmark" method="post">' \
                    '<input type="text" name="title" required=true placeholder="Title"><br>' \
                    '<input type="text" name="description" placeholder="Description (optional)">' \
                    '<br>' \
                    '<input type="text" name="url" required=true placeholder="URL"><br>' \
                    '<input type="submit">' \
                '</form>' \
                "<hr>"

            all_bookmarks = self.server.get_all_bookmarks()
            for b in all_bookmarks:
                html += f"<b>{b.title}:</b> "
                # description is optional
                if b.description:
                    html += f"{b.description} "
                html += f"<a href={b.url} target=\"_blank\">{b.url}</a><br>"

            return html

        @self.app.route('/')
        def index():
            return main_page_html()

        @self.app.route('/add_bookmark', methods=["POST"])
        def add_bookmark():
            title = request.form.get("title")
            description = request.form.get("description")
            url = request.form.get("url")
            logger.info("got request to add bookmark: title=%s, desc=%s, url=%s",
                        title, description, url)
            self.server.add_bookmark(title, description, url)
            return main_page_html()

    def run(self, host, port):
        self.app.run(host=host, port=port)
