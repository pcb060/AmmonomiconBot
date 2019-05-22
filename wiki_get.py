from bs4 import BeautifulSoup
import requests

ETG_ENDPOINT = "https://enterthegungeon.gamepedia.com/"
MINIMUM_P_LENGTH = 10


def get_wiki_entry(item):
    return parse_content(item)


def parse_content(item):
    page = requests.get(ETG_ENDPOINT + item).content
    soup = BeautifulSoup(page, 'html.parser')
    try:
        ps = soup.table.extract()  # rimuove la tabella di "riassunto" dal contenuto parsato
    except:
        print("Nessuna <table> trovata.")
    finally:
        ps = soup.find("div", {"class": "mw-parser-output"}).find_all("p")
        description = str(remove_fake_p_entries(ps)[0])
        description = recreate_links(description)
    return description


def remove_fake_p_entries(list):
    new_list = []
    for item in list:
        # ignoro <p> con immagini o semplicemente vuoti
        if "<img" not in str(item) and len(str(item)) > MINIMUM_P_LENGTH:
            new_list.append(item)

    return new_list


def recreate_links(content):
    return content.replace("<a href=\"/", "<a href=\"https://enterthegungeon.gamepedia.com/")
