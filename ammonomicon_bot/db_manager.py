from tinydb import TinyDB, Query
from fuzzywuzzy import fuzz
from utils import check_if_infinite, check_if_multiple_qualities

db = TinyDB("ammonomicon_bot/dbs/db.json")

last_item_inserted = None


# Icon | Name | Base Health | Description
def upsert_enemy(parsed_entry):
    """Query the db for an entry of type "enemy" and update it if it already exists, insert it if it doesn't
    """
    Enemy = Query()

    this_enemy = {
        "Category": "Enemy",
        "Icon": parsed_entry[0].find("img")["src"],
        "Name": parsed_entry[1].get_text().replace("\n", ""),
        "Base Health": parsed_entry[2].get_text().replace("\n", ""),
        "Description": parsed_entry[3].get_text().replace("\n", ""),
    }

    db.upsert(this_enemy, Enemy["Name"] == this_enemy["Name"])


# Icon | Name | Quote | Qlty | Type | MagSize | AmmoCap | Dmg | FireRate | RldTime | ShotSpd | Rng | Frc | Sprd | Notes
def upsert_gun(parsed_entry):
    """Query the db for an entry of type "gun" and update it if it already exists, insert it if it doesn't
    """
    Gun = Query()

    this_gun = {
        "Category": "Gun",
        "Icon": parsed_entry[0].find("img")["src"],
        "Name": parsed_entry[1].get_text().replace("\n", ""),
        "Quote": parsed_entry[2].get_text().replace("\n", ""),
        "Quality": (
            parsed_entry[3]
            .find("img")["alt"]
            .replace(" Quality Item.png", "")
            .replace("1S", "S")
            if parsed_entry[3].find("img")["alt"].startswith("1")
            else parsed_entry[3].find("img")["alt"].replace(" Quality Item.png", "")
        ),
        "Type": parsed_entry[4].get_text().replace("\n", ""),
        "Magazine Size": check_if_infinite(parsed_entry[5]),
        "Ammo Capacity": check_if_infinite(parsed_entry[6]),
        "Damage": parsed_entry[7].get_text().replace("\n", ""),
        "Fire Rate": parsed_entry[8].get_text().replace("\n", ""),
        "Reload Time": parsed_entry[9].get_text().replace("\n", ""),
        "Shot Speed": check_if_infinite(parsed_entry[10]),
        "Range": check_if_infinite(parsed_entry[11]),
        "Force": parsed_entry[12].get_text().replace("\n", ""),
        "Spread": parsed_entry[13].get_text().replace("\n", ""),
        "Notes": parsed_entry[14].get_text().replace("\n", ""),
    }

    db.upsert(this_gun, Gun["Name"] == this_gun["Name"])


# Icon | Name | Type | Quote | Quality | Effect
def upsert_item(parsed_entry):
    """Query the db for an entry of type "item" and update it if it already exists, insert it if it doesn't
    """
    Item = Query()
    global last_item_inserted

    # default case
    if len(parsed_entry) == 6:
        this_item = {
            "Category": "Item",
            "Icon": parsed_entry[0].find("img")["src"],
            "Name": parsed_entry[1].get_text().replace("\n", ""),
            "Type": parsed_entry[2].get_text().replace("\n", ""),
            "Quote": parsed_entry[3].get_text().replace("\n", ""),
            "Quality": check_if_multiple_qualities(parsed_entry[4]),
            "Effect": parsed_entry[5].get_text().replace("\n", ""),
        }
    # ruby bracelet special case
    elif last_item_inserted["Name"] == "Ruby Bracelet":
        this_item = {
            "Category": "Item",
            "Icon": last_item_inserted["Icon"],
            "Name": last_item_inserted["Name"] + "(Upgraded)",
            "Type": last_item_inserted["Type"],
            "Quote": parsed_entry[0].get_text().replace("\n", ""),
            "Quality": last_item_inserted["Quality"],
            "Effect": parsed_entry[1].get_text().replace("\n", ""),
        }

    db.upsert(
        this_item,
        Item["Name"] == this_item["Name"] and Item["Quote"] == this_item["Quote"],
    )
    last_item_inserted = this_item


def get_entry(name):
    """Uses fuzzy search inside database for entries matching name and returns most likely candidate
    """
    res = db.all()

    max = 0
    ind = 0
    for match in res:
        f = fuzz.ratio(res[ind]["Name"], name)
        if f > max:
            max = f
            most_likely = res[ind]
        ind += 1

    print(
        'SEARCH: Most likely: "' + most_likely["Name"] + '", fuzz value = ' + str(max)
    )
    return most_likely

