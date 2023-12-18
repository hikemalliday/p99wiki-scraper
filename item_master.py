from bs4 import BeautifulSoup
import json
import requests
import omit
import sqlite3
import config
import parse_functions
import asyncio
import aiohttp

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

async def item_master_data_scrape(item: dict) -> dict or None:
    item_name = list(item.keys())[0]
    item_url = item[item_name]
    error_object = {item_url: {}}
    error_flag = False
    async with aiohttp.ClientSession() as session:
        async with session.get(item_url) as response:
            if response.status == 200:
                print(f'item_master_data_scrape(): {item_name}')
                soup = BeautifulSoup(await response.text(), "html.parser")
                item_object = parse_functions.get_item_object(soup, item_name)
                
                for key, value in item_object.items():
                    if value == 'Error':
                        error_flag = True
                        error_object[item_url][key] = value
                        value = None
                
                if error_flag == True:
                    with open('./data/item_master_error_log.json', 'r') as item_error_log_raw:
                        item_error_log_new = json.load(item_error_log_raw)
                        item_error_log_new.append(error_object)
                
                    with open('./data/item_master_error_log.json', 'w') as item_error_log:
                        json.dump(item_error_log_new, item_error_log, indent=2)

                properties = {
                    'MAGIC ITEM': False,
                    'LORE ITEM': False,
                    'NO DROP': False,
                    'NO RENT': False,
                    'EXPENDABLE': False,
                    'QUEST': False
                }

                if item_object['Properties']:
                    for prop in item_object['Properties']:
                        properties[prop] = True

                char_classes = {
                    'ENC': False,
                    'MAG': False,
                    'NEC': False,
                    'WIZ': False,
                    'CLR': False,
                    'DRU': False,
                    'SHM': False,
                    'BRD': False,
                    'MNK': False,
                    'RNG': False,
                    'ROG': False,
                    'PAL': False,
                    'SHD': False,
                    'WAR': False,
                }

                if item_object['Class']:
                    for char_class in item_object['Class']:
                        char_classes[char_class] = True
                
                char_races = {
                    'BAR': False,
                    'DEF': False,
                    'DWF': False,
                    'ERU': False,
                    'GNM': False,
                    'HEF': False,
                    'HFL': False,
                    'HIE': False,
                    'HUM': False,
                    'IKS': False,
                    'OGR': False,
                    'TRL': False,
                    'ELF': False,
                }

                if item_object['Race']:
                    for char_race in item_object['Race']:
                        char_races[char_race] = True

                item_slots = {
                    'PRIMARY': False,
                    'SECONDARY': False,
                    'RANGE': False,
                    'ARMS': False,
                    'BACK': False,
                    'CHEST': False,
                    'EAR': False,
                    'FACE': False,
                    'FEET': False,
                    'FINGERS': False,
                    'HANDS': False,
                    'HEAD': False,
                    'LEGS': False,
                    'NECK': False,
                    'SHOULDERS': False,
                    'WAIST': False,
                    'WRIST': False,
                    'AMMO': False,
                }

                if item_object['Slots']:
                    for slot in item_object['Slots']:
                        item_slots[slot] = True
                
                conn = sqlite3.connect(config.database)
                c = conn.cursor()
                try:
                    c.execute(''' INSERT INTO item_master (
                            item_name,
                            item_magic,
                            item_lore,
                            item_no_drop,
                            item_no_rent,
                            item_expendable,
                            item_quest,
                            item_dmg,
                            item_delay,
                            item_ac,
                            item_effect,
                            item_hp,
                            item_mp,
                            item_str,
                            item_sta,
                            item_dex,
                            item_agi,
                            item_wis,
                            item_int,
                            item_cha,
                            item_sv_fire,
                            item_sv_disease,
                            item_sv_cold,
                            item_sv_magic,
                            item_sv_poison,
                            item_wt,
                            item_size,
                            item_image
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                        ''', (
                            item_object['Item Name'], 
                            properties['MAGIC ITEM'], 
                            properties['LORE ITEM'], 
                            properties['NO DROP'], 
                            properties['NO RENT'], 
                            properties['EXPENDABLE'], 
                            properties['QUEST'], 
                            item_object['DMG'], 
                            item_object['Atk Delay'], 
                            item_object['AC'], 
                            item_object['Effect'], 
                            item_object['HP'], 
                            item_object['MP'], 
                            item_object['STR'], 
                            item_object['STA'], 
                            item_object['DEX'], 
                            item_object['AGI'], 
                            item_object['WIS'], 
                            item_object['INT'], 
                            item_object['CHA'], 
                            item_object['SV_FIRE'], 
                            item_object['SV_DISEASE'], 
                            item_object['SV_COLD'], 
                            item_object['SV_MAGIC'], 
                            item_object['SV_POISON'], 
                            item_object['WT'], 
                            item_object['Size'], 
                            item_object['Item Image'], 
                            ));
                    
                    item_id = c.lastrowid
                    c.execute('''INSERT INTO item_class (
                            item_id,
                            item_enc,
                            item_mag,
                            item_nec,
                            item_wiz,
                            item_clr,
                            item_dru,
                            item_shm,
                            item_brd,
                            item_mnk,
                            item_rng,
                            item_rog,
                            item_pal,
                            item_shd,
                            item_war
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        item_id,
                        char_classes['ENC'],
                        char_classes['MAG'],
                        char_classes['NEC'],
                        char_classes['WIZ'],
                        char_classes['CLR'],
                        char_classes['DRU'],
                        char_classes['SHM'],
                        char_classes['BRD'],
                        char_classes['MNK'],
                        char_classes['RNG'],
                        char_classes['ROG'],
                        char_classes['PAL'],
                        char_classes['SHD'],
                        char_classes['WAR']
                        ));
                    
                    c.execute('''INSERT INTO item_race (
                            item_id,
                            item_bar,
                            item_def,
                            item_dwf,
                            item_eru,
                            item_gnm,
                            item_hef,
                            item_hfl,
                            item_hie,
                            item_hum,
                            item_iks,
                            item_ogr,
                            item_trl,
                            item_elf
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        item_id,
                        char_races['BAR'],
                        char_races['DEF'],
                        char_races['DWF'],
                        char_races['ERU'],
                        char_races['GNM'],
                        char_races['HEF'],
                        char_races['HFL'],
                        char_races['HIE'],
                        char_races['HUM'],
                        char_races['IKS'],
                        char_races['OGR'],
                        char_races['TRL'],
                        char_races['ELF'],
                        ));
                    
                    c.execute('''INSERT INTO item_slot (
                            item_id,
                            item_primary,
                            item_secondary,
                            item_range,
                            item_arms,
                            item_back,
                            item_chest,
                            item_ear,
                            item_face,
                            item_feet,
                            item_fingers,
                            item_hands,
                            item_head,
                            item_legs,
                            item_neck,
                            item_shoulders,
                            item_waist,
                            item_wrist,
                            item_ammo
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        item_id,
                        item_slots['PRIMARY'],
                        item_slots['SECONDARY'],
                        item_slots['RANGE'],
                        item_slots['ARMS'],
                        item_slots['BACK'],
                        item_slots['CHEST'],
                        item_slots['EAR'],
                        item_slots['FACE'],
                        item_slots['FEET'],
                        item_slots['FINGERS'],
                        item_slots['HANDS'],
                        item_slots['HEAD'],
                        item_slots['LEGS'],
                        item_slots['NECK'],
                        item_slots['SHOULDERS'],
                        item_slots['WAIST'],
                        item_slots['WRIST'],
                        item_slots['AMMO'],
                        ));
                    
                    conn.commit()
                    conn.close()
                   
                    with open("./data/latest_item_master_parse.json", "w") as latest_parse_json:
                        json.dump([{item_name: item_url}], latest_parse_json, indent=2)
                    return item_object
                except sqlite3.Error as e:
                    print(f"SQLite error: {e}")
                    conn.rollback()
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                print(f'Failed to retrieve data from {item_url}')
                return None
                   
async def item_master_scrape():
    with open("./data/item_urls.json", "r") as item_urls:
        data = json.load(item_urls)
    with open("./data/latest_item_master_parse.json", "r") as latest_parse_json:
        latest_parse_json = json.load(latest_parse_json)
        if latest_parse_json:
            latest_parsed_object = latest_parse_json[-1]
            latest_parsed_item_name = list(latest_parsed_object.keys())[0]
            found_latest_item = False
            while found_latest_item == False:
                for index, item_object in enumerate(data):
                    keys = list(item_object.keys())
                    key = keys[0]
                    if key == latest_parsed_item_name:
                        found_latest_item = True
                        data = data[index:]
                        print('Match found, resuming parse from "latest parsed"...')
                        break      
        else:
            found_latest_item = True
        semaphore = asyncio.Semaphore(8)

        async def limited_task(item):
            async with semaphore:
                return await item_master_data_scrape(item)
        
        tasks = [limited_task(item) for item in data]
        results = await asyncio.gather(*tasks)

        for result in results:
            if result:
                print(result)

if __name__ == "__main__":
    asyncio.run(item_master_scrape())