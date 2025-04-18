import base64
import logging
import json
from enum import Enum

from flask import Flask, request, redirect, url_for, flash, get_flashed_messages

from utils import opts, version
from utils.html_utils import html_escape
from app.app_sections import BookmarkSection, StatusSection


INC_URL_DEFAULT = "false"
IS_FUZZY_DEFAULT = "true"
FAVORITES_ONLY_DEFAULT = "false"

logger = logging.getLogger()


class Route (Enum):
    INDEX = "/"
    BOOKMARKS = "/bookmarks"
    ADD_BOOKMARK = "/add_bookmark"
    EDIT_FORM = "/edit"  # edit form (GET)
    EDIT_BOOKMARK = "/edit_bookmark"  # edit and display all (POST)
    TOGGLE_FAVORITED = "/toggleFavorited"
    DELETE_BOOKMARK = "/delete_bookmark"
    IMPORT = "/import"
    ABOUT = "/about"


class Page (Enum):
    HOME = "Home"
    IMPORT = "Import"
    ABOUT = "About"


class BookmarkFormType (Enum):
    ADD = "Add"
    EDIT = "Edit"


page_to_route = {
    Page.HOME: Route.INDEX.value,
    Page.IMPORT: Route.IMPORT.value,
    Page.ABOUT: Route.ABOUT.value,
}
assert len(Page) == len(page_to_route)


def get_favorite_star_color(is_favorited):
    if is_favorited:
        return "red"
    else:
        return "lightgray"


class AppAPI:
    # pylint: disable=R0915, R0914 (too-many-statements, too-many-locals)
    def __init__(self, app, default_fuzzy_search):
        self.app = app
        self.default_fuzzy_search = default_fuzzy_search
        self.app_api = Flask(__name__)
        self.app_api.secret_key = 'secretkey'

        def _status_to_color(status):
            return "green" if status.success else "red"

        def _bookmark_form(bookmark_form_type, bookmark_section, sections):
            """A form to add/edit a bookmark."""
            if not bookmark_section:
                bookmark_section = BookmarkSection("", "", "", "", None)

            html = f'<h4>{bookmark_form_type.value} a bookmark</h4>'
            html += f'<form action="/{bookmark_form_type.value.lower()}_bookmark" method="post">'

            if bookmark_section.bookmark_id is not None:
                html += '<input type="hidden" id="bookmark_id" name="bookmark_id" ' \
                        f'value="{bookmark_section.bookmark_id}" />'

            html += f'<input type="text" name="section" list="sections" placeholder="Section" ' \
                    f'size="50" value="{html_escape(bookmark_section.last_section)}"><br>' \
                    f'<input type="text" name="title" placeholder="* Title" ' \
                    f'size="50" value="{html_escape(bookmark_section.last_title)}"><br>' \
                    f'<input type="text" name="description" placeholder="Description" ' \
                    f'size="50" value="{html_escape(bookmark_section.last_description)}"><br>' \
                    f'<input type="text" name="url" placeholder="* URL" ' \
                    f'size="50" value="{html_escape(bookmark_section.last_url)}"><br>' \
                    f'<datalist id="sections">'
            for s in sections:
                html += f'<option>{s}</option>'
            html += '</datalist>' \
                '<input onclick="this.form.submit();this.disabled = true;" type="submit">' \
                '</form>'

            return html

        def _search_section():
            checked = "checked" if self.default_fuzzy_search else ""
            fuzzy_checkbox = f'<input type="checkbox" id="fuzzy" {checked}>'
            return """
                <br>
                Search:
                <br>
                <textarea id="searchBookmark" name="searchBookmark" rows="3" cols="30"></textarea><br>
                <br>

                """ \
                + fuzzy_checkbox + \
                """
                <label for="fuzzy"> Fuzzy search</label><br>

                <input type="checkbox" id="includeurl">
                <label for="includeurl"> Include URL</label><br>

                <input type="checkbox" id="favoritesonly">
                <label for="favoritesonly"> Favorites only</label><br>

                <br>

                <script type="text/javascript">
                  function searchEvent()
                  {
                    patterns = document.getElementById("searchBookmark").value;
                    fuzzy = document.getElementById("fuzzy").checked;
                    include_url = document.getElementById("includeurl").checked;
                    favorites_only = document.getElementById("favoritesonly").checked;

                    const xhttp = new XMLHttpRequest();
                    xhttp.onload = function() {
                      document.getElementById("bookmarks_div").innerHTML = this.responseText;

                      // eval the scripts
                      const scripts = document.querySelectorAll('#bookmarks_div script');
                      scripts.forEach(script => {
                        eval(script.textContent);
                      });
                    }
                    xhttp.open("GET", "/bookmarks?pattern=" + btoa(patterns) +
                      "&fuzzy=" + fuzzy +
                      "&includeurl=" + include_url +
                      "&favoritesonly=" + favorites_only);
                    xhttp.send();
                  }

                  fuzzy.addEventListener("input", searchEvent);
                  includeurl.addEventListener("input", searchEvent);
                  favoritesonly.addEventListener("input", searchEvent);
                  searchBookmark.addEventListener("input", searchEvent);

                  window.onkeydown = function(e) {
                    // ctrl-b - set focus on search input
                    if (e.keyCode == 66 && e.ctrlKey) {
                      document.getElementById("searchBookmark").focus();
                      document.getElementById("searchBookmark").select();
                    }
                    // ESC - reset search
                    else if (e.key === "Escape") {
                      document.getElementById("searchBookmark").value = '';
                      searchEvent()
                    }
                  }
                </script>
            """

        def _header():
            return f'<h1 style="text-align:center">' \
                   f'<a href="/" style="color:black; text-decoration: none;">{opts.PROD_NAME}</a>' \
                   f'</h1>'

        def _menu(curr_page):
            html = '<p style="text-align:center"><b>'

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

        def _bookmarks_section(display_bookmarks_section):
            bookmarks_section = '<body style="overflow-wrap: break-word;">'
            bookmarks_section += '<div id="bookmarks_div">'

            if display_bookmarks_section.bookmarks is not None:
                # icon library
                bookmarks_section += '<link rel="stylesheet" ' \
                    'href="https://cdnjs.cloudflare.com' \
                    '/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">'
                # delete bookmark function
                bookmarks_section += """
                    <script>
                      function copyURL(url)
                      {
                        navigator.clipboard.writeText(url);
                      }

                      function deleteBookmark(bookmark_id)
                      {
                        if (confirm('Delete bookmark?')) {
                          var delete_form = document.createElement('form');
                          delete_form.action='/delete_bookmark';
                          delete_form.method='POST';

                          var inpt=document.createElement('input');
                          inpt.type='hidden';
                          inpt.name='bookmark_id';
                          inpt.value=bookmark_id
                          delete_form.appendChild(inpt);

                          document.body.appendChild(delete_form);
                          delete_form.submit();
                        } else {
                          return False
                        }
                      }

                      function toggle_favorited(bookmark_id)
                      {
                        const xhttp = new XMLHttpRequest();
                        xhttp.onload = function() {
                          document.getElementById("favoriteStar_" + bookmark_id).style.color = this.responseText;
                        }
                        xhttp.open("POST", "/toggleFavorited?bookmark_id=" + bookmark_id);
                        xhttp.send();
                      }
                    </script>
                """

                bookmarks_section += f"Total: {len(display_bookmarks_section.bookmarks)}<br><br>"

                prev_section = None
                for b in display_bookmarks_section.bookmarks:
                    if b.section and b.section != prev_section:
                        prev_section = b.section
                        bookmarks_section += f"<br><u><b><b>{b.escaped_section}</b></u><br>"

                    bookmarks_section += f'<button class="btn" onclick="copyURL(\'{b.escaped_url}\')">' \
                        '<i class="fa fa-copy"></i></button> '
                    bookmarks_section += '<button class="btn" ' \
                        f'onclick="window.location.href=\'{Route.EDIT_FORM.value}?id={b.id}\'">' \
                        '<i class="fa fa-edit"></i></button> '
                    bookmarks_section += f'<button class="btn" onclick="deleteBookmark({b.id})">' \
                        '<i class="fa fa-trash"></i></button> '
                    star_color = get_favorite_star_color(b.is_favorited)
                    bookmarks_section += f'<span id="favoriteStar_{b.id}" style="color:{star_color}; cursor:pointer;">&#9733;</span> <!-- Star symbol -->'
                    bookmarks_section += '<script>' \
                        f'document.getElementById("favoriteStar_{b.id}").addEventListener("click", function()' \
                        '{' \
                        f'  toggle_favorited({b.id});' \
                        '});' \
                      '</script>'

                    bookmarks_section += f"<b>{b.escaped_title}:</b> "
                    # description is optional
                    if b.description:
                        bookmarks_section += f"{b.escaped_description} "
                    bookmarks_section += f"<a href={b.escaped_url} target=\"_blank\">{b.escaped_url}</a><br>"
            else:
                bookmarks_section = \
                    f'<div style="color:red">{display_bookmarks_section.display_bookmarks_err}</div>'

            bookmarks_section += '<br></div>'

            bookmarks_section += '</body>'
            return bookmarks_section

        def _status_section(status_section):
            if not status_section:
                return ""
            return f'<div style="color:{_status_to_color(status_section)}">{status_section.msg}</div>'

        def _main_page(status_section, display_bookmarks_section, add_bookmark_section):
            # prepare list of sections
            sections = []
            if display_bookmarks_section.bookmarks:
                prev_section = None
                for b in display_bookmarks_section.bookmarks:
                    if b.section != prev_section:
                        if not b.section:
                            continue
                        prev_section = b.section
                        sections.append(b.section)

            return _header() + \
                _menu(Page.HOME) + \
                _status_section(status_section) + \
                _bookmark_form(BookmarkFormType.ADD, add_bookmark_section, sections) + \
                "<hr>" + \
                _search_section() + \
                _bookmarks_section(display_bookmarks_section)

        @self.app_api.route(Route.BOOKMARKS.value)
        def bookmark():
            patterns = request.args.get("pattern")
            if patterns:
                patterns = base64.b64decode(patterns).decode('utf-8')
                patterns = patterns.splitlines()
            else:
                patterns = []

            is_fuzzy = request.args.get("fuzzy", IS_FUZZY_DEFAULT)
            is_fuzzy = is_fuzzy.lower() == "true"
            include_url = request.args.get("includeurl", INC_URL_DEFAULT)
            include_url = include_url.lower() == "true"
            favorites_only = request.args.get("favoritesonly", FAVORITES_ONLY_DEFAULT)
            favorites_only = favorites_only.lower() == "true"

            return _bookmarks_section(self.app.display_bookmarks(patterns, is_fuzzy, include_url, favorites_only))

        @self.app_api.route(Route.INDEX.value)
        def index():
            pattern = request.args.get("pattern")
            patterns = [pattern] if pattern else []

            is_fuzzy = request.args.get("fuzzy", IS_FUZZY_DEFAULT)
            is_fuzzy = is_fuzzy.lower() == "true"
            include_url = request.args.get("includeurl", INC_URL_DEFAULT)
            include_url = include_url.lower() == "true"
            favorites_only = request.args.get("favoritesonly", FAVORITES_ONLY_DEFAULT)
            favorites_only = favorites_only.lower() == "true"

            status_section = None
            status_msg = get_flashed_messages()
            if status_msg:
                status_json = json.loads(status_msg[0])
                status_section = StatusSection(status_json["success"], status_json["msg"])

            return _main_page(status_section, self.app.display_bookmarks(patterns, is_fuzzy, include_url, favorites_only), None)

        def flash_status_and_redirect(status_section):
            status_json = {
                "success": status_section.success,
                "msg": status_section.msg
            }
            flash(json.dumps(status_json))
            return redirect(url_for('index'))

        @self.app_api.route(Route.ADD_BOOKMARK.value, methods=["POST"])
        def add_bookmark():
            title = request.form.get("title")
            description = request.form.get("description")
            url = request.form.get("url")
            section = request.form.get("section")

            status_section, display_bookmarks_section, bookmark_section = \
                self.app.add_bookmark(title, description, url, section)
            if status_section.success:
                return flash_status_and_redirect(status_section)
            else:
                # if request failed, we don't redirect in order to preserve the input fields
                return _main_page(status_section, display_bookmarks_section, bookmark_section)

        def _display_edit_form(title, description, url, section, bookmark_id, status_section):
            bookmark_section = BookmarkSection(title, description, url, section, bookmark_id)
            sections = {}
            return _header() + \
                _menu(None) + \
                _status_section(status_section) + \
                _bookmark_form(BookmarkFormType.EDIT, bookmark_section, sections)

        @self.app_api.route(Route.EDIT_FORM.value)
        def edit_form():
            bookmark_id = request.args.get("id")
            bookmark = self.app.edit_bookmark_form(bookmark_id)
            if not bookmark:
                return _main_page(None, self.app.display_bookmarks(None, False, False, False), None)

            return _display_edit_form(bookmark.title, bookmark.description, bookmark.url, bookmark.section, bookmark_id, None)

        @self.app_api.route(Route.EDIT_BOOKMARK.value, methods=["POST"])
        def edit_bookmark():
            bookmark_id = request.form.get("bookmark_id")
            title = request.form.get("title")
            description = request.form.get("description")
            url = request.form.get("url")
            section = request.form.get("section")
            status_section, display_bookmarks_section, bookmark_section = \
                self.app.edit_bookmark(bookmark_id, title, description, url, section)

            if not status_section.success:
                return _display_edit_form(title, description, url, section, bookmark_id, status_section)

            return flash_status_and_redirect(status_section)

        @self.app_api.route(Route.TOGGLE_FAVORITED.value, methods=["POST"])
        def toggle_facorited():
            bookmark_id = request.args.get("bookmark_id")
            is_favorited = self.app.toggle_favorited(bookmark_id)
            return get_favorite_star_color(is_favorited)

        @self.app_api.route(Route.DELETE_BOOKMARK.value, methods=["POST"])
        def delete_bookmark():
            bookmark_id = request.form.get("bookmark_id")
            status_section, display_section = self.app.delete_bookmark(bookmark_id)
            return flash_status_and_redirect(status_section)

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
