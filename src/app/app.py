from flask import Flask

from server import bookmarks


class App:
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        def hello_world():
            return "EasyBookmarks"

    def run(self, host, port):
        self.app.run(host=host, port=port)
