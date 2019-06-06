from bs4 import BeautifulSoup
import requests
from ammonomicon_bot.conf.endpoints import *
import ammonomicon_bot.db_manager as dbm
from ammonomicon_bot.utils import row_to_list_of_cells


def parse_enemies():
    """Parse content inside enemies' table @ http://enterthegungeon.gamepedia.com/Enemies
    """
    page = requests.get(ENEMIES_ENDPOINT).content
    soup = BeautifulSoup(page, "html.parser")

    rows = soup.find("table").find_all("tr")
    rows.pop(0)  # removes table header containing field names

    for row in rows:
        dbm.upsert_enemy(row_to_list_of_cells(row))


def parse_guns():
    """Parse content inside guns' table @ http://enterthegungeon.gamepedia.com/Guns
    """
    page = requests.get(GUNS_ENDPOINT).content
    soup = BeautifulSoup(page, "html.parser")

    rows = soup.find("table").find_all("tr")
    rows.pop(0)  # removes table header containing field names

    for row in rows:
        dbm.upsert_gun(row_to_list_of_cells(row))


def parse_items():
    """Parse content inside items' table @ http://enterthegungeon.gamepedia.com/Items
    """
    page = requests.get(ITEMS_ENDPOINT).content
    soup = BeautifulSoup(page, "html.parser")

    rows = soup.find("table").find_all("tr")
    rows.pop(0)  # removes table header containing field names

    for row in rows:
        dbm.upsert_item(row_to_list_of_cells(row))
