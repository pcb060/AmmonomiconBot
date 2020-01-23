from conf.endpoints import ETG_WIKI_ENDPOINT
from conf.help_urls import *
import md_formatter as md


def row_to_list_of_cells(parsed_row):
    """Returns list of cells composing row
    """
    tmp = list()
    for cell in parsed_row:
        # ignores empty cells
        if str(cell) != "\n":
            tmp.append(cell)
    return tmp


def check_if_infinite(parsed_cell):
    """Returns "∞" if cell contains Infinity png, else parses value as usual
    """
    if parsed_cell.find_all("img") and parsed_cell.find("img")["alt"] == "Infinity.png":
        return "∞"
    else:
        return parsed_cell.get_text().replace("\n", "")


def check_if_multiple_qualities(parsed_cell):
    """Checks if cell contains multiple Quality Item png's. Returns string with found qualities.
    """
    qlt = ""
    counter = 0
    if len(parsed_cell.find_all("img")) > 1:
        for item in parsed_cell.find_all("img"):
            if counter >= 1:
                qlt += ", "
            qlt += (
                item["alt"].replace(" Quality Item.png", "").replace("1", "")
                if item["alt"].startswith("1")
                else item["alt"].replace(" Quality Item.png", "")
            )
            counter += 1
    else:
        qlt = (
            str(parsed_cell.find("img")["alt"]).replace(" Quality Item.png", "")
            if item["alt"].startswith("1")
            else item["alt"].replace(" Quality Item.png", "")
        )
    return qlt


def format_to_comment(entry):
    """Checks entry category and returns string with info formatted accordingly (using markdown syntax)
    """
    comm = ""

    if entry["Category"] == "Enemy":
        # 1st block: Name
        comm += md.bold(md.link(entry["Name"], entry["Icon"])) + "\n"
        # 2nd block: Notes
        comm += md.quote(entry["Description"]) + "\n"
        # 3rd block: Quality and Type (Base Health)
        comm += md.bold("Base Health:") + " " + entry["Base Health"] + "\n\n"
        # 4th block: Link to wiki
        comm += (
            "For more information, see the "
            + md.link(
                "official entry in the wiki.",
                ETG_WIKI_ENDPOINT + entry["Name"].replace(" ", "_"),
            )
            + "\n"
        )

    elif entry["Category"] == "Gun":
        # 1st block: Name and Quote
        comm += md.bold(md.link(entry["Name"], entry["Icon"]))
        comm += " - " + md.italic(entry["Quote"]) + "\n"
        # 2nd block: Notes
        comm += md.quote(entry["Notes"]) + "\n"
        # 3rd block: Quality and Type
        comm += (
            md.bold("Quality:")
            + " "
            + entry["Quality"]
            + " | "
            + md.bold("Type:")
            + " "
            + entry["Type"]
            + "\n\n"
        )
        # 4th block: Characteristics
        elements = [
            md.bold("Magazine Size:") + " " + entry["Magazine Size"],
            md.bold("Ammo Capacity:") + " " + entry["Ammo Capacity"],
            md.bold("Damage:") + " " + entry["Damage"],
            md.bold("Fire Rate:") + " " + entry["Fire Rate"],
            md.bold("Reload Time:") + " " + entry["Reload Time"],
            md.bold("Shot Speed:") + " " + entry["Shot Speed"],
            md.bold("Range:") + " " + entry["Range"],
            md.bold("Force:") + " " + entry["Force"],
            md.bold("Spread:") + " " + entry["Spread"],
        ]
        comm += md.unordered_list(elements) + "\n"
        # 5th block: link to wiki
        comm += (
            "For more information, see the "
            + md.link(
                "official entry in the wiki.",
                ETG_WIKI_ENDPOINT + entry["Name"].replace(" ", "_"),
            )
            + "\n"
        )

    elif entry["Category"] == "Item":
        # 1st block: Name and Quote
        comm += md.bold(md.link(entry["Name"], entry["Icon"]))
        comm += " - " + md.italic(entry["Quote"]) + "\n"
        # 2nd block: Notes
        comm += md.quote(entry["Effect"]) + "\n"
        # 3rd block: Quality and Type
        comm += (
            md.bold("Quality:")
            + " "
            + entry["Quality"]
            + " | "
            + md.bold("Type:")
            + " "
            + entry["Type"]
            + "\n\n"
        )
        # 4th block: Link to wiki
        comm += (
            "For more information, see the "
            + md.link(
                "official entry in the wiki.",
                ETG_WIKI_ENDPOINT + entry["Name"].replace(" ", "_"),
            )
            + "\n"
        )

    return comm


def comment_help():
    return (
        md.hr()
        + "\n"
        + md.hr()
        + "\n"
        + md.link(md.superscript("FAQ"), FAQ_URL)
        + " ^| "
        + md.link(md.superscript("Mistake?"), MISTAKE_URL)
        + " ^| "
        + md.link(md.superscript("Github"), GITHUB_URL)
        + " ^| "
        + md.link(md.superscript("Support me"), SUPPORT_ME_URL)
    )

