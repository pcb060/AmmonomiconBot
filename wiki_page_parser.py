from bs4 import BeautifulSoup
import requests

ETG_ENDPOINT = "https://enterthegungeon.gamepedia.com/"
MINIMUM_P_LENGTH = 10  # kinda arbitrary atm


def get_entry(item):
    page = requests.get(ETG_ENDPOINT + item).content
    soup = BeautifulSoup(page, "html.parser")
    try:
        # removes "summary" table from parsed content
        ps = soup.table.extract()
    except:
        print("No <table> element found.")
    finally:
        ps = soup.find("div", {"class": "mw-parser-output"}).find_all("p")
        description = str(remove_fake_p_entries(ps)[0])
        description = recreate_links(description)
    return description


def remove_fake_p_entries(list):
    new_list = []
    for item in list:
        # ignores <p>'s with pictures / empty ones
        if "<img" not in str(item) and len(str(item)) > MINIMUM_P_LENGTH:
            new_list.append(item)

    return new_list


def recreate_links(content):
    return content.replace(
        '<a href="/', '<a href="https://enterthegungeon.gamepedia.com/'
    )
