from flask import escape


def html_escape(text):
    if not text:
        return text
    return escape(text)


def split_escaped_text(line):
    res = []

    escaped_opened = False
    for c in line:
        if escaped_opened:
            res[-1] += c
            if c == ";":
                escaped_opened = False
        else:
            res.append(c)
            if c == "&":
                escaped_opened = True

    return res


def highlight(line_list, indexes):
    if not line_list:
        return ""
    if not indexes:
        return "".join(line_list)

    highlighted_line = ""
    for i, c in enumerate(line_list):
        if i in indexes:
            highlighted_line += f"<mark>{c}</mark>"
        else:
            highlighted_line += c
    return "".join(highlighted_line)
