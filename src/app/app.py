import logging

from flask import Flask, request

from utils import opts
from server.server_api import InternalException
from server.bookmarks import html_escape


GET_BOOKMARKS_ERR_MSG = "Internal error: failed to read bookmarks. Please try again later"
ADD_BOOKMARK_ERR_MSG = "Internal error: failed to add a new bookmark. Please try again later"
ADD_BOOKMARK_OK_MSG = "Bookmark added successfully"
ADD_BOOKMARK_TITLE_REQUIRED_MSG = "Error: Title is a required field"
ADD_BOOKMARK_URL_REQUIRED_MSG = "Error: URL is a required field"

logger = logging.getLogger()


class App:
    def __init__(self, server):
        self.server = server
        self.app = Flask(__name__)

        def _add_bookmark_form(add_bookmark_msg, add_title_val, add_description_val, add_url_val):
            html = '<h4>Add a new bookmark</h4>'
            if add_bookmark_msg:
                html += f'{add_bookmark_msg}'
            html += f'<form action="/add_bookmark" method="post">' \
                    f'<input type="text" name="title" required=true placeholder="* Title" ' \
                    f'size="50" value="{html_escape(add_title_val)}"><br>' \
                    f'<input type="text" name="description" placeholder="Description" ' \
                    f'size="50" value="{html_escape(add_description_val)}"><br>' \
                    f'<input type="text" name="url" required=true placeholder="* URL" ' \
                    f'size="50" value="{html_escape(add_url_val)}"><br>' \
                    f'<input type="submit">' \
                f'</form>' \
                f"<hr>"
            return html

        def _main_page_html(
                add_bookmark_msg=None,
                add_title_val="",
                add_description_val="",
                add_url_val=""):
            # header
            html = f'<h1 style="text-align:center">{opts.PROD_NAME}</h1>'

            # add bookmark form
            html += _add_bookmark_form(
                add_bookmark_msg, add_title_val, add_description_val, add_url_val)

            # display bookmarks
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
                html += f'<div style="color:red">{GET_BOOKMARKS_ERR_MSG}</div>'

            return html

        @self.app.route('/')
        def index():
            return _main_page_html()

        @self.app.route('/add_bookmark', methods=["POST"])
        def add_bookmark():
            title = request.form.get("title")
            description = request.form.get("description")
            url = request.form.get("url")

            # input validation
            # not expected to happen because browser enforces it (using HTML 'required' attribute)
            if not title or not url:
                add_bookmark_msg = f'<div style="color:red">{ADD_BOOKMARK_TITLE_REQUIRED_MSG}</div>' \
                    if not title else f'<div style="color:red">{ADD_BOOKMARK_URL_REQUIRED_MSG}</div>'
                return _main_page_html(add_bookmark_msg=add_bookmark_msg,
                                       add_title_val=title,
                                       add_description_val=description,
                                       add_url_val=url)

            logger.info("got request to add bookmark: title=%s, desc=%s, url=%s",
                        title, description, url)
            try:
                self.server.add_bookmark(title, description, url)
                add_bookmark_msg = f'<div style="color:green">{ADD_BOOKMARK_OK_MSG}</div>'
                return _main_page_html(add_bookmark_msg=add_bookmark_msg)
            except InternalException:
                add_bookmark_msg = f'<div style="color:red">{ADD_BOOKMARK_ERR_MSG}</div>'
                return _main_page_html(add_bookmark_msg=add_bookmark_msg,
                                       add_title_val=title,
                                       add_description_val=description,
                                       add_url_val=url)

    def run(self, host, port):
        self.app.run(host=host, port=port)
