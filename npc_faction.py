from bs4 import BeautifulSoup
import json
import requests
import sqlite3
import config
import parse_functions
import omit
import aiohttp
import asyncio

async def npc_faction_scrape():
    with open('./data/npc_urls.json', 'r') as npc_urls:
        data = json.load(npc_urls)
    with open('./data/latest_npc_faction_parse.json', 'r') as latest_parse_json:
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
                return await npc_faction_data_scrape(npc)
            
        tasks = [limited_task(npc) for npc in data]
        results = await asyncio.gather(*tasks)

        for result in results:
            if result:
                print(result)
            
async def npc_faction_data_scrape(npc: dict) -> dict or None:
    npc_name = list(npc.keys())[0]
    npc_url = npc[npc_name]
    error_object = {npc_url: {}}
    error_flag = False
    async with aiohttp.ClientSession() as session:
        async with session.get(npc_url) as response:
            if response.status == 200:
                print(f'npc_faction_data_scrape(): {npc_name}')
                soup = BeautifulSoup(await response.text(), "html.parser")
                npc_object = {
                    "Factions": parse_functions.get_npc_factions(soup),
                    "Opposing factions": parse_functions.get_npc_opposing_factions(soup),
                }

                for key, value in npc_object.items():
                    if value == 'Error':
                        error_flag = True
                        error_object[npc_url][key] = value
                        value = None

                if error_flag == True:
                    with open('./data/npc_faction_error_log.json', 'r') as npc_error_log_raw:
                        npc_error_log_new = json.load(npc_error_log_raw)
                        npc_error_log_new.append(error_object)

                    with open('./data/npc_faction_error_log.json', 'w') as npc_error_log:
                        json.dump(npc_error_log_new, npc_error_log, indent=2)
                try:
                    conn = sqlite3.connect(config.database)
                    c = conn.cursor()
                    print(npc_name)
                    c.execute("""SELECT npc_id FROM npc_master WHERE npc_name = ?""", (npc_name,))
                    npc_id = c.fetchone()[0];
                    if not npc_id:
                        print('NPC not found, aborting parse for now...')
                        return
                    print("Factions:")
                    print(npc_object['Factions'])
                    print("Opposing factions:")
                    print(npc_object['Opposing factions'])
                    
                    # Factions:
                    for faction_name, faction_hit in npc_object['Factions']:
                        if any(faction_name == value for value in omit.omit_these):
                            continue
                        if any(faction_hit == value for value in omit.omit_these):
                            faction_hit = None
                        faction_id = None
                        c.execute("""SELECT faction_id FROM faction_master WHERE faction_name = ?""", (faction_name,))
                        faction_id = c.fetchone()
                        if faction_id:
                            faction_id = faction_id[0]
                        else:
                            c.execute("""INSERT OR IGNORE INTO faction_master (faction_name) VALUES (?)""", (faction_name,))
                            c.execute("""SELECT faction_id FROM faction_master WHERE faction_name = ?""", (faction_name,))
                            new_faction_result = c.fetchone()
                            if new_faction_result:
                                faction_id = new_faction_result[0]
                        if faction_id:
                            c.execute("""INSERT INTO npc_faction (faction_id, npc_id, hit) VALUES (?, ?, ?)""", (faction_id, npc_id, faction_hit))

                    # Opposing factions:
                    for faction_name, faction_hit in npc_object['Opposing factions']:
                        if any(faction_name == value for value in omit.omit_these):
                            continue
                        if any(faction_hit == value for value in omit.omit_these):
                            faction_hit = None
                        faction_id = None
                        c.execute("""SELECT faction_id FROM faction_master WHERE faction_name = ?""", (faction_name,))
                        faction_id = c.fetchone()
                        if faction_id:
                            faction_id = faction_id[0]
                        else:
                            c.execute("""INSERT OR IGNORE INTO faction_master (faction_name) VALUES (?)""", (faction_name,))
                            c.execute("""SELECT faction_id FROM faction_master WHERE faction_name = ?""", (faction_name,))
                            new_faction_result = c.fetchone()
                            if new_faction_result:
                                faction_id = new_faction_result[0]
                        if faction_id:
                            c.execute("""INSERT INTO npc_faction (faction_id, npc_id, hit) VALUES (?, ?, ?)""", (faction_id, npc_id, faction_hit))
                    conn.commit()
                    conn.close()
                    with open('./data/latest_npc_faction_parse.json', 'w') as latest_parse_json:
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
    asyncio.run(npc_faction_scrape())