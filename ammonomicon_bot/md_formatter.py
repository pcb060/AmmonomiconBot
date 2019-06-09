def link(text, url):
    """Returns markdown string with text linking to url
    """
    return "[" + text + "](" + url + ")"


def superscript(text):
    """Returns markdown string with superscripted text
    """
    return "^(" + text + ")"


def italic(text):
    """Returns markdown string with italicized text
    """
    return "*" + text + "*"


def bold(text):
    """Returns markdown string with bolded text
    """
    return "**" + text + "**"


def quote(text):
    """Returns markdown string with quoted text
    """
    return ">" + text


def unordered_list(elements):
    """Returns markdown string with unordered list, one bullet for each element inside elements
    """
    final = str()
    for e in elements:
        final += "* " + elements[e] + "\n"
    return final


def hr():
    """Returns markdown string with horizontal rule
    """
    return "___"
