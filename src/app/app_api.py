from flask import Flask, request

from utils import opts


class AppAPI:
    def __init__(self, app):
        self.app = app
        self.app_api = Flask(__name__)

        def _add_bookmark_form(add_bookmark_succeeded, add_bookmark_msg,
                               add_title_val, add_description_val, add_url_val):
            html = '<h4>Add a new bookmark</h4>'
            if add_bookmark_succeeded in (True, False):
                color = "green" if add_bookmark_succeeded else "red"
                html += f'<div style="color:{color}">{add_bookmark_msg}</div>'
            html += f'<form action="/add_bookmark" method="post">' \
                    f'<input type="text" name="title" required=true placeholder="* Title" ' \
                    f'size="50" value="{add_title_val}"><br>' \
                    f'<input type="text" name="description" placeholder="Description" ' \
                    f'size="50" value="{add_description_val}"><br>' \
                    f'<input type="text" name="url" required=true placeholder="* URL" ' \
                    f'size="50" value="{add_url_val}"><br>' \
                    f'<input type="submit">' \
                f'</form>' \
                f"<hr>"
            return html

        def _main_page(add_bookmark_succeeded, add_bookmark_msg,
                       add_title_val, add_description_val, add_url_val,
                       bookmarks, get_bookmarks_err):
            header = f'<h1 style="text-align:center">{opts.PROD_NAME}</h1>'

            add_bookmark_form = _add_bookmark_form(add_bookmark_succeeded, add_bookmark_msg,
                                                   add_title_val, add_description_val, add_url_val)

            bookmarks_section = ""
            if bookmarks is not None:
                bookmarks_section += f"Total: {len(bookmarks)}<br><br>"

                for b in bookmarks:
                    bookmarks_section += f"<b>{b.title}:</b> "
                    # description is optional
                    if b.description:
                        bookmarks_section += f"{b.description} "
                    bookmarks_section += f"<a href={b.url} target=\"_blank\">{b.url}</a><br>"
            else:
                bookmarks_section = f'<div style="color:red">{get_bookmarks_err}</div>'

            return header + add_bookmark_form + bookmarks_section

        @self.app_api.route('/')
        def index():
            add_bookmark_succeeded, add_bookmark_msg, \
                add_title_val, add_description_val, add_url_val, \
                bookmarks, get_bookmarks_err \
                = self.app.get_bookmarks()
            return _main_page(add_bookmark_succeeded, add_bookmark_msg,
                              add_title_val, add_description_val, add_url_val,
                              bookmarks, get_bookmarks_err)

        @self.app_api.route('/add_bookmark', methods=["POST"])
        def add_bookmark():
            title = request.form.get("title")
            description = request.form.get("description")
            url = request.form.get("url")
            add_bookmark_succeeded, add_bookmark_msg, \
                add_title_val, add_description_val, add_url_val, \
                bookmarks, get_bookmarks_err \
                = self.app.add_bookmark(title, description, url)
            return _main_page(add_bookmark_succeeded, add_bookmark_msg,
                              add_title_val, add_description_val, add_url_val,
                              bookmarks, get_bookmarks_err)

    def run(self, host, port):
        self.app_api.run(host=host, port=port)  # blocking
