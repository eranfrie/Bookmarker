from flask import Flask, request

from utils import opts


PAGE_HOME = "Home"
PAGE_IMPORT = "Import"
pages = {
    PAGE_HOME: "/",
    PAGE_IMPORT: "/import",
}


class AppAPI:
    def __init__(self, app):
        self.app = app
        self.app_api = Flask(__name__)

        def _add_bookmark_form(add_bookmark_section):
            html = '<h4>Add a new bookmark</h4>'
            if add_bookmark_section.last_op_succeeded in (True, False):
                color = "green" if add_bookmark_section.last_op_succeeded else "red"
                html += f'<div style="color:{color}">{add_bookmark_section.last_op_msg}</div>'
            html += f'<form action="/add_bookmark" method="post">' \
                    f'<input type="text" name="title" required=true placeholder="* Title" ' \
                    f'size="50" value="{add_bookmark_section.last_title}"><br>' \
                    f'<input type="text" name="description" placeholder="Description" ' \
                    f'size="50" value="{add_bookmark_section.last_description}"><br>' \
                    f'<input type="text" name="url" required=true placeholder="* URL" ' \
                    f'size="50" value="{add_bookmark_section.last_url}"><br>' \
                    f'<input type="submit">' \
                f'</form>' \
                f"<hr>"
            return html

        def _header():
            return f'<h1 style="text-align:center">{opts.PROD_NAME}</h1>'

        def _menu(curr_page):
            html = '<p  style="text-align:center"><b>'

            first_page = True
            for p, url in pages.items():
                if first_page:
                    first_page = False
                else:
                    html += ' | '

                if p == curr_page:
                    html += p
                else:
                    html += f'<a href={url} style="color:black">' + p + '</a>'

            html += '</b></h1>'
            return html

        def _main_page(display_bookmarks_section, add_bookmark_section, curr_page):
            add_bookmark_form = _add_bookmark_form(add_bookmark_section)

            bookmarks_section = ""
            if display_bookmarks_section.bookmarks is not None:
                bookmarks_section += f"Total: {len(display_bookmarks_section.bookmarks)}<br><br>"

                for b in display_bookmarks_section.bookmarks:
                    bookmarks_section += f"<b>{b.title}:</b> "
                    # description is optional
                    if b.description:
                        bookmarks_section += f"{b.description} "
                    bookmarks_section += f"<a href={b.url} target=\"_blank\">{b.url}</a><br>"
            else:
                bookmarks_section = \
                    f'<div style="color:red">{display_bookmarks_section.display_bookmarks_err}</div>'

            return _header() + _menu(curr_page) + add_bookmark_form + bookmarks_section

        @self.app_api.route('/')
        def index():
            display_bookmarks_section, add_bookmark_section = self.app.display_bookmarks()
            return _main_page(display_bookmarks_section, add_bookmark_section, PAGE_HOME)

        @self.app_api.route('/add_bookmark', methods=["POST"])
        def add_bookmark():
            title = request.form.get("title")
            description = request.form.get("description")
            url = request.form.get("url")

            display_bookmarks_section, add_bookmark_section = self.app.add_bookmark(title, description, url)
            return _main_page(display_bookmarks_section, add_bookmark_section, PAGE_IMPORT)

        @self.app_api.route('/import')
        def import_bookmarks():
            import_section = '<h4>Import bookmarks</h4>'
            import_section += "TBD ..."

            return _header() + _menu(PAGE_IMPORT) + import_section

    def run(self, host, port):
        self.app_api.run(host=host, port=port)  # blocking
