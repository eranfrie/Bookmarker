import logging
from enum import Enum

from flask import Flask, request

from utils import opts, version


logger = logging.getLogger()


class Route (Enum):
    INDEX = "/"
    ADD_BOOKMARK = "/add_bookmark"
    IMPORT = "/import"
    ABOUT = "/about"


class Page (Enum):
    HOME = "Home"
    IMPORT = "Import"
    ABOUT = "About"


page_to_route = {
    Page.HOME: Route.INDEX.value,
    Page.IMPORT: Route.IMPORT.value,
    Page.ABOUT: Route.ABOUT.value,
}
assert len(Page) == len(page_to_route)


class AppAPI:
    # pylint: disable=R0915 (too-many-statements)
    def __init__(self, app):
        self.app = app
        self.app_api = Flask(__name__)

        def _add_bookmark_form(add_bookmark_section):
            html = '<h4>Add a new bookmark</h4>'
            if add_bookmark_section.last_op_succeeded in (True, False):
                color = "green" if add_bookmark_section.last_op_succeeded else "red"
                html += f'<div style="color:{color}">{add_bookmark_section.last_op_msg}</div>'
            html += f'<form action="/add_bookmark" method="post">' \
                    f'<input type="text" name="title" placeholder="* Title" ' \
                    f'size="50" value="{add_bookmark_section.last_title}"><br>' \
                    f'<input type="text" name="description" placeholder="Description" ' \
                    f'size="50" value="{add_bookmark_section.last_description}"><br>' \
                    f'<input type="text" name="url" placeholder="* URL" ' \
                    f'size="50" value="{add_bookmark_section.last_url}"><br>' \
                    f'<input type="text" name="section" placeholder="Section" ' \
                    f'size="50" value="{add_bookmark_section.last_section}"><br>' \
                    f'<input type="submit">' \
                f'</form>' \
                f"<hr>"
            return html

        def _search_form():
            html = '<form action="/">' \
                   '<label for="search">Search:</label>' \
                   '<input type="search" id="pattern" name="pattern">' \
                   '<input type="submit" value="Go">' \
                   '</form>'
            return html

        def _header():
            return f'<h1 style="text-align:center">{opts.PROD_NAME}</h1>'

        def _menu(curr_page):
            html = '<p  style="text-align:center"><b>'

            first_page = True
            for page, url in page_to_route.items():
                if first_page:
                    first_page = False
                else:
                    html += ' | '

                if page == curr_page:
                    html += page.value
                else:
                    html += f'<a href={url} style="color:black">' + page.value + '</a>'

            html += '</b></h1>'
            return html

        def _main_page(display_bookmarks_section, add_bookmark_section):
            add_bookmark_form = _add_bookmark_form(add_bookmark_section)

            bookmarks_section = ""
            if display_bookmarks_section.bookmarks is not None:
                bookmarks_section += f"Total: {len(display_bookmarks_section.bookmarks)}<br><br>"

                bookmarks_section += _search_form()

                prev_section = None
                for b in display_bookmarks_section.bookmarks:
                    if b.section and b.section != prev_section:
                        prev_section = b.section
                        bookmarks_section += f"<br><u><b><b>{b.section}</b></u><br>"
                    bookmarks_section += f"<b>{b.title}:</b> "
                    # description is optional
                    if b.description:
                        bookmarks_section += f"{b.description} "
                    bookmarks_section += f"<a href={b.url} target=\"_blank\">{b.url}</a><br>"
            else:
                bookmarks_section = \
                    f'<div style="color:red">{display_bookmarks_section.display_bookmarks_err}</div>'

            return _header() + _menu(Page.HOME) + add_bookmark_form + bookmarks_section

        @self.app_api.route(Route.INDEX.value)
        def index():
            pattern = request.args.get("pattern")
            display_bookmarks_section, add_bookmark_section = self.app.display_bookmarks(pattern)
            return _main_page(display_bookmarks_section, add_bookmark_section)

        @self.app_api.route(Route.ADD_BOOKMARK.value, methods=["POST"])
        def add_bookmark():
            title = request.form.get("title")
            description = request.form.get("description")
            url = request.form.get("url")
            section = request.form.get("section")

            display_bookmarks_section, add_bookmark_section = self.app.add_bookmark(
                    title, description, url, section)
            return _main_page(display_bookmarks_section, add_bookmark_section)

        @self.app_api.route(Route.IMPORT.value, methods=["GET", "POST"])
        def import_bookmarks():
            last_op_html = ""

            if request.method == "POST":
                f = request.files.get("bookmarks_html")
                err, num_added, num_failed = self.app.import_bookmarks(f)
                if err:
                    last_op_html = '<div style="color:red">Failed to import bookmarks</div>'
                else:
                    if num_added > 0:
                        last_op_html += f'<div style="color:green">Imported {num_added} bookmarks</div>'
                    if num_failed > 0:
                        last_op_html += \
                                f'<div style="color:red">Failed to import {num_failed} bookmarks</div>'

            import_section = '<h4>Import bookmarks</h4>'
            import_section += last_op_html
            import_section += '<form action="/import" method="post" enctype = "multipart/form-data">'
            import_section += '<input type="file" name="bookmarks_html">'
            import_section += '<input type="submit">'
            import_section += '</form>'

            return _header() + _menu(Page.IMPORT) + import_section

        @self.app_api.route(Route.ABOUT.value)
        def about():
            about_section = '<h4>About</h4>'

            ver = version.get_version()
            about_section += f'{opts.PROD_NAME} Version {ver}<br/>'

            home_page = "https://github.com/eranfrie/Bookmarker"
            about_section += f'Home page: <a href="{home_page}" target="_blank">{home_page}</a>'

            return _header() + _menu(Page.ABOUT) + about_section

    def run(self, host, port):
        self.app_api.run(host=host, port=port)  # blocking
