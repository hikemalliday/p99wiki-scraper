from bs4 import BeautifulSoup
import json
import requests
import omit
import sqlite3
import config
import parse_functions
import os
import asyncio
import aiohttp

proprties = ['MAGIC ITEM', 'LORE ITEM', 'NO DROP', 'EXPENDABLE', 'QUEST ITEM', 'NO RENT']

def create_item_urls_json(item_urls: list):
    with open("./data/item_urls.json", "w") as json_file:
        json.dump(item_urls, json_file, indent=2)
    print('./data/item_urls.JSON created.')

def item_url_scrape():
    next_page = True
    item_list = []
    item_object = {}
    next_url = ''
    first_url = "https://wiki.project1999.com/Category:Items"
    while next_page:
        if next_url != '':
            response = requests.get(next_url, verify=False)
        else:
            response = requests.get(first_url, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            #item_names = soup.find_all('a')
            items_element = soup.find("h2", text='Pages in category "Items"')
            if items_element:
                print('test')
                item_names = items_element.find_parent().find_all('a')
            for name in item_names:
                if name.text in omit.item_scrape_omit:
                    continue
                item_object[name.text] = config.base_url + "/" +name.text.replace(' ', '_').replace("`", '%60')
                item_list.append(item_object)
                item_object = {}
            next_link = soup.find('a', string='next 200')
            if next_link:
                next_url = config.base_url + next_link.get('href')
                print("Next URL:, next_url")
            else:
                print("Next page not found, ending loop")
                break
        else:
            print(f"Error: Unable to fetch the webpage. Status code: {response.status_code}")
    print("Scraping complete, calling 'create_item_urls_json()'...")
    create_item_urls_json(item_list)


# TODO:
# This is a work in progress / rough draft: 
async def item_data_scrape(item: dict) -> dict or None:
    item_name = list(item.keys())[0]
    item_url = item[item_name]
    async with aiohttp.ClientSession() as session:
        async with session.get(item_url) as response:
            if response.status == 200:
                print(f'scraping {item_name}')
                soup = BeautifulSoup(await response.text(), "html.parser")
                parse_functions.get_item_img(soup, item_name)
                item_object = {
                    "Item Name": item_name,
                    "Properties": parse_functions.get_item_properties(soup),
                    "Slot": parse_functions.get_item_slot(soup),
                    "Class": parse_functions.get_item_class(soup),
                    "Race": parse_functions.get_item_race(soup),
                    "DMG": parse_functions.get_item_dmg(soup),
                    "Atk Delay": parse_functions.get_item_delay(soup),
                    "AC": parse_functions.get_item_ac(soup),
                    "Effect": parse_functions.get_item_effect(soup),
                    "HP": parse_functions.get_item_hp(soup),
                    "MP": parse_functions.get_item_mp(soup),
                    "STR": parse_functions.get_item_str(soup),
                    "STA": parse_functions.get_item_sta(soup),
                    "DEX": parse_functions.get_item_dex(soup),
                    "AGI": parse_functions.get_item_agi(soup),
                    "WIS": parse_functions.get_item_wis(soup),
                    "INT": parse_functions.get_item_int(soup),
                    "CHA": parse_functions.get_item_cha(soup),
                    "SV_FIRE": parse_functions.get_item_resists(soup, 'SV_FIRE'),
                    "SV_DISEASE": parse_functions.get_item_resists(soup, 'SV_DISEASE'),
                    "SV_COLD": parse_functions.get_item_resists(soup, 'SV_COLD'),
                    "SV_MAGIC": parse_functions.get_item_resists(soup, 'SV_MAGIC'),
                    "SV_POISON": parse_functions.get_item_resists(soup, 'SV_POISON'),
                    "WT": parse_functions.get_item_wt(soup),
                    "Size": parse_functions.get_item_size(soup),
                    }
                return item_object
            else:
                print(f'Failed to retrieve data from {item_url}')
                return None
            
async def item_master_scrape():
    counter = 0
    with open("./data/item_urls.json", "r") as item_urls:
        # master_error_list = []
        # item_array = []
        # item_json = []
        data = json.load(item_urls)
        semaphore = asyncio.Semaphore(8)

        async def limited_task(item):
            async with semaphore:
                return await item_data_scrape(item)
        
        tasks = [limited_task(item) for item in data]
        results = await asyncio.gather(*tasks)

        for result in results:
            if result is not None:
                print(result)

if __name__ == "__main__":
    asyncio.run(item_master_scrape())