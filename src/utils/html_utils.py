from flask import escape


def html_escape(text):
    if not text:
        return text
    return escape(text)
