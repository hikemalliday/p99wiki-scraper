from bs4 import BeautifulSoup
import json
import requests
import omit
import sqlite3
import config
import parse_functions
import aiohttp
import asyncio

def create_npc_urls_json(npc_urls: list):
    with open("./data/npc_urls.json", "w") as json_file:
        json.dump(npc_urls, json_file, indent=2)
    print('./data/npc_urls.JSON created.')
    
def npc_url_scrape():
    next_page = True
    npcs_list = []
    npc_object = {}
    next_url = ''
    first_url = "https://wiki.project1999.com/Category:NPCs"
    while next_page:
        if next_url != '':
            response = requests.get(next_url, verify=False)
        else:
            response = requests.get(first_url, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            npc_names = soup.find_all('a')
            for name in npc_names:
                if name.text in omit.npc_scrape_omit:
                    continue
                npc_object[name.text] = config.base_url + '/' + name.text.replace(' ', '_').replace("`", '%60')
                npcs_list.append(npc_object)
                npc_object = {}
            next_link = soup.find('a', string='next 200')
            if next_link:
                next_url = config.base_url + next_link.get('href')
                print('Next URL:', next_url)
            else:
                print("Next page not found, ending loop.")
                break
        else:
            print(f'Error: Unable to fetch the webpage. Status code: {response.status_code}')
    print('Scraping complete, calling "create_npc_urls_json()"...')
    create_npc_urls_json(npcs_list)

async def npc_master_scrape():
    with open('./data/npc_urls.json', 'r') as npc_urls:
        data = json.load(npc_urls)
    with open('./data/latest_npc_master_parse.json', 'r') as latest_parse_json:
        latest_parse_json = json.load(latest_parse_json)
        if latest_parse_json:
            latest_parsed_object = latest_parse_json[-1]
            latest_parsed_npc_name = list(latest_parsed_object.keys())[0]
            found_latest_npc = False
            while found_latest_npc == False:
                for index, npc_object in enumerate(data):
                    keys = list(npc_object.keys())
                    key = keys[0]
                    if key == latest_parsed_npc_name:
                        found_latest_npc = True
                        data = data[index:]
                        print('Match found, resuming parse from "latest parsed"...')
                        break
        else:
            found_latest_npc = True
        semaphore = asyncio.Semaphore(8)

        async def limited_task(npc):
            async with semaphore:
                return await npc_master_data_scrape(npc)
            
        tasks = [limited_task(npc) for npc in data]
        results = await asyncio.gather(*tasks)

        for result in results:
            if result:
                print(result)

async def npc_master_data_scrape(npc: dict) -> dict or None:
    npc_name = list(npc.keys())[0]
    npc_url = npc[npc_name]
    error_object = {npc_url: {}}
    async with aiohttp.ClientSession() as session:
        async with session.get(npc_url) as response:
            if response.status == 200:
                print(f'npc_master_data_scrape(): {npc_name}')
                soup = BeautifulSoup(await response.text(), "html.parser")
                npc_object = parse_functions.get_npc_master_object(soup, npc_name)

                for key, value in npc_object.items():
                    if value == 'Error':
                        error_object[npc_url][key] = value
                        value = None
                
                with open('./data/npc_master_error_log.json', 'r') as npc_error_log_raw:
                    npc_error_log_new = json.load(npc_error_log_raw)
                    npc_error_log_new.append(error_object)

                with open('./data/npc_master_error_log.json', 'w') as npc_error_log:
                    json.dump(npc_error_log_new, npc_error_log, indent=2)
            
                try:
                    conn = sqlite3.connect(config.database)
                    c = conn.cursor()
                    c.execute("""INSERT INTO npc_master (npc_name, npc_description, npc_race, npc_class, npc_min_level, npc_max_level, npc_respawn_time, npc_AC, npc_HP, npc_min_damage_per_hit, npc_max_damage_per_hit, npc_attacks_per_round) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                            (npc_object['Name'], 
                            npc_object['Description'],
                            npc_object['Race'], 
                            npc_object['Class'], 
                            npc_object['Level'][0], 
                            npc_object['Level'][1], 
                            npc_object['Respawn'],
                            npc_object['AC'],
                            npc_object['HP'],
                            npc_object['Damage per hit'][0],
                            npc_object['Damage per hit'][1],
                            npc_object['Attacks per round'],
                            ))
                    conn.commit()
                    conn.close()

                    with open('./data/latest_npc_master_parse.json', 'w') as latest_parse_json:
                        json.dump([{npc_name: npc_url}], latest_parse_json, indent=2)
                    return npc_object
                except sqlite3.Error as e:
                    print(f'SQLite error: {e}')
                except Exception as e:
                    print(f'An error occurred: {e}')
            else:
                print(f'Failed to retrieve data fom {npc_url}')
                return None
            
if __name__ == "__main__":
    asyncio.run(npc_master_scrape())

   






