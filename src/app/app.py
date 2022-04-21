import logging

from flask import Flask, request

from server.server_api import InternalException


logger = logging.getLogger()

GET_BOOKMARKS_ERR_MSG = "Internal error: failed to read bookmarks. please try again later"
ADD_BOOKMARK_ERR_MSG = "Internal error: failed to add a new bookmark. please try again later"
ADD_BOOKMARK_OK_MSG = "Bookmark added successfully"
ADD_BOOKMARK_TITLE_REQUIRED_MSG = "Title is a required field"
ADD_BOOKMARK_URL_REQUIRED_MSG = "URL is a required field"


class App:
    def __init__(self, server):
        self.server = server
        self.app = Flask(__name__)

        def main_page_html(add_bookmark_msg=None):
            html = "<h1>EasyBookmarks</h1>"

            # add bookmark form
            html += '<h4>Add a new bookmark</h4>'
            if add_bookmark_msg:
                html += f'{add_bookmark_msg}'
            html += '<form action="/add_bookmark" method="post">' \
                    '<input type="text" name="title" required=true placeholder="Title"><br>' \
                    '<input type="text" name="description" placeholder="Description (optional)">' \
                    '<br>' \
                    '<input type="text" name="url" required=true placeholder="URL"><br>' \
                    '<input type="submit">' \
                '</form>' \
                "<hr>"

            try:
                all_bookmarks = self.server.get_all_bookmarks()
                total_bookmarks = len(all_bookmarks)
                html += f"Total: {total_bookmarks}<br><br>"

                for b in all_bookmarks:
                    html += f"<b>{b.title}:</b> "
                    # description is optional
                    if b.description:
                        html += f"{b.description} "
                    html += f"<a href={b.url} target=\"_blank\">{b.url}</a><br>"
            except InternalException:
                html += f'<p style="color:red">{GET_BOOKMARKS_ERR_MSG}</p>'

            return html

        @self.app.route('/')
        def index():
            return main_page_html()

        @self.app.route('/add_bookmark', methods=["POST"])
        def add_bookmark():
            title = request.form.get("title")
            if not title:
                add_bookmark_msg = f'<p style="color:red">{ADD_BOOKMARK_TITLE_REQUIRED_MSG}</p>'
                return main_page_html(add_bookmark_msg=add_bookmark_msg)
            description = request.form.get("description")
            url = request.form.get("url")
            if not url:
                add_bookmark_msg = f'<p style="color:red">{ADD_BOOKMARK_URL_REQUIRED_MSG}</p>'
                return main_page_html(add_bookmark_msg=add_bookmark_msg)
            logger.info("got request to add bookmark: title=%s, desc=%s, url=%s",
                        title, description, url)

            try:
                self.server.add_bookmark(title, description, url)
                add_bookmark_msg = f'<p style="color:green">{ADD_BOOKMARK_OK_MSG}</p>'
            except InternalException:
                add_bookmark_msg = f'<p style="color:red">{ADD_BOOKMARK_ERR_MSG}</p>'

            return main_page_html(add_bookmark_msg=add_bookmark_msg)

    def run(self, host, port):
        self.app.run(host=host, port=port)
