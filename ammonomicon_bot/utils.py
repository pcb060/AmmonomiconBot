import urllib.parse
from ammonomicon_bot.conf.endpoints import *
import ammonomicon_bot.md_formatter as md


def row_to_list_of_cells(parsed_row):
    tmp = list()
    for cell in parsed_row:
        if str(cell) != "\n":
            tmp.append(cell)
    return tmp


def check_if_infinite(parsed_cell):
    if parsed_cell.find_all("img") and parsed_cell.find("img")["alt"] == "Infinity.png":
        return "∞"
    else:
        return parsed_cell.get_text().replace("\n", "")


def check_if_multiple_qualities(parsed_cell):
    qlt = ""
    counter = 0
    if len(parsed_cell.find_all("img")) > 1:
        for item in parsed_cell.find_all("img"):
            if counter >= 1:
                qlt += ", "
            qlt += item["alt"].replace(" Quality Item.png", "")
            counter += 1
    else:
        qlt = str(parsed_cell.find("img")["alt"]).replace(" Quality Item.png", "")
    return qlt


def format_to_comment(entry):
    comm = None
    if entry["Category"] == "Enemy":
        # 1st block
        comm += entry["Name"] + md.superscript(
            md.bold(md.link("sprite", entry["Icon"]))
        )
        comm += " - " + md.italic(entry["Quote"]) + "\n"
        # 2nd block
        comm += md.quote(entry["Notes"]) + "\n"
        # 3rd block
        comm += (
            "Quality: "
            + md.bold(entry["Quality"])
            + " | Type: "
            + md.bold(entry["Type"])
            + "\n"
        )
        # 4th block
        elements = [
            md.bold("Magazine Size: ") + entry["Magazine Size"],
            md.bold("Ammo Capacity: ") + entry["Ammo Capacity"],
            md.bold("Damage: ") + entry["Damage"],
            md.bold("Fire Rate: ") + entry["Fire Rate"],
            md.bold("Reload Time: ") + entry["Reload Time"],
            md.bold("Shot Speed: ") + entry["Shot Speed"],
            md.bold("Range: ") + entry["Range"],
            md.bold("Force: ") + entry["Force"],
            md.bold("Spread: ") + entry["Spread"],
        ]
        comm += md.unordered_list(elements) + "\n"
        # 5th block
        comm += (
            "For more information, see the "
            + md.link(
                "official entry in the wiki.",
                ETG_WIKI_ENDPOINT + urllib.parse.quote(entry["Name"]),
            )
            + "\n"
        )
        # 6th block
        comm += md.hr()
        comm += md.superscript("FAQ | Mistake? | Github | Support me")

    elif entry["Category"] == "Gun":
        pass

    elif entry["Category"] == "Item":
        pass

    return ""
