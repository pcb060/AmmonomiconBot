from bs4 import BeautifulSoup
import requests
from ammonomicon_bot.conf.endpoints import *
import ammonomicon_bot.db_manager as dbm


def parse_enemies():
    """Parse content inside enemies' table @ enterthegungeon.gamepedia.com/Enemies
    """
    page = requests.get(ENEMIES_ENDPOINT).content
    soup = BeautifulSoup(page, "html.parser")

    rows = soup.find("table").find_all("tr")
    rows.pop(0)  # removes table header containing field names

    for row in rows:
        dbm.load_parsed_enemy_into_db(row)


def parse_guns():
    """Parse content inside guns' table @ enterthegungeon.gamepedia.com/Guns
    """
    page = requests.get(GUNS_ENDPOINT).content
    soup = BeautifulSoup(page, "html.parser")

    rows = soup.find("table").find_all("tr")
    rows.pop(0)  # removes table header containing field names

    for row in rows:
        dbm.load_parsed_gun_into_db(row)


def parse_items():
    """Parse content inside items' table @ enterthegungeon.gamepedia.com/Items
    """
    page = requests.get(ITEMS_ENDPOINT).content
    soup = BeautifulSoup(page, "html.parser")

    rows = soup.find("table").find_all("tr")
    rows.pop(0)  # removes table header containing field names

    for row in rows:
        dbm.load_parsed_item_into_db(row)
