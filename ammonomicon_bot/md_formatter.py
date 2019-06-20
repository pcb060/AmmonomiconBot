def link(text, url):
    """Returns markdown string for text linking to url
    """
    return "[" + text + "](" + url + ")"


def superscript(text):
    """Returns markdown string for superscripted text
    """
    return "^(" + text + ")"


def italic(text):
    """Returns markdown string for italicized text
    """
    return "*" + text.strip() + "*"


def bold(text):
    """Returns markdown string for bolded text
    """
    return "**" + text.strip() + "**"


def quote(text):
    """Returns markdown string for quoted text
    """
    return ">" + text + "\n"


def unordered_list(elements):
    """Returns markdown string for unordered list, one bullet for each element inside elements
    """
    final = str()
    ind = 0
    for e in elements:
        final += "* " + elements[ind] + "\n"
        ind += 1
    return final


def hr():
    """Returns markdown string for horizontal rule
    """
    return "___"
