from tinydb import TinyDB, Query

db = TinyDB("ammonomicon_bot/dbs/db.json")

# initialize tables
enemies_table = db.table("Enemies")
guns_table = db.table("Guns")
items_table = db.table("Items")


# Icon | Name | Base Health | Description
def load_parsed_enemy_into_db(parsed_entry):
    Enemy = Query()

    tmp = list()
    for cell in parsed_entry:
        if str(cell) != "\n":
            tmp.append(cell)

    this_enemy = {
        "Icon": tmp[0].find("img")["src"],
        "Name": tmp[1].get_text().replace("\n", ""),
        "Base Health": tmp[2].get_text().replace("\n", ""),
        "Description": tmp[3].get_text().replace("\n", ""),
    }

    enemies_table.upsert(this_enemy, Enemy["Name"] == this_enemy["Name"])


# Icon | Name | Quote | Qlty | Type | MagSize | AmmoCap | Dmg | FireRate | RldTime | ShotSpd | Rng | Frc | Sprd | Notes
def load_parsed_gun_into_db(parsed_entry):
    Gun = Query()

    tmp = list()
    for cell in parsed_entry:
        cell = str(cell)
        if cell != "\n":
            tmp.append(cell)

    gun = {
        "Icon": tmp[0],
        "Name": tmp[1],
        "Quote": tmp[2],
        "Quality": tmp[3],
        "Type": tmp[4],
        "Magazine Size": tmp[5],
        "Ammo Capacity": tmp[6],
        "Damage": tmp[7],
        "Fire Rate": tmp[8],
        "Reload Time": tmp[9],
        "Shot Speed": tmp[10],
        "Range": tmp[10],
        "Force": tmp[11],
        "Spread": tmp[12],
        "Notes": tmp[13],
    }

    guns_table.upsert(gun, Gun["Name"] == tmp[1])


# Icon | Name | Type | Quote | Quality | Effect
def load_parsed_item_into_db(parsed_entry):
    Item = Query()

    tmp = list()
    for cell in parsed_entry:
        cell = str(cell)
        if cell != "\n":
            tmp.append(cell)

    item = {
        "Icon": tmp[0],
        "Name": tmp[1],
        "Type": tmp[2],
        "Quote": tmp[3],
        "Quality": tmp[4],
        "Effect": tmp[5],
    }

    items_table.upsert(item, Item["Name"] == tmp[1])
