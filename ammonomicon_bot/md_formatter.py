def link(text, url):
    return "[" + text + "](" + url + ")"


def superscript(text):
    return "^(" + text + ")"


def italic(text):
    return "*" + text + "*"


def bold(text):
    return "**" + text + "**"


def quote(text):
    return ">" + text


def unordered_list(elements):
    final = str()
    for e in elements:
        final += "* " + elements[e] + "\n"
    return final


def hr():
    return "___"
