from bs4 import BeautifulSoup
import json
import requests
import sqlite3
import config
import parse_functions
import asyncio
import aiohttp

async def npc_zone_data_scrape(npc: dict) -> dict or None:
    npc_name = list(npc.keys())[0]
    npc_url = npc[npc_name]
    error_object = {npc_url: {}}
    error_flag = False
    async with aiohttp.ClientSession() as session:
        async with session.get(npc_url) as response:
            if response.status == 200:
                print(f'npc_master_data_scrape(): {npc_name}')
                soup = BeautifulSoup(await response.text(), "html.parser")
                npc_object = {
                    "Zone": parse_functions.get_npc_zone(soup),
                }

                for key, value in npc_object.items():
                    if value == 'Error':
                        error_flag = True
                        error_object[npc_url][key] = value
                        value = None

                if error_flag == True:
                    with open('./data/npc_zone_error-log.json', 'r') as npc_error_log_raw:
                        npc_error_log_new = json.load(npc_error_log_raw)
                        npc_error_log_new.append(error_object)

                    with open('./data/npc_zone_error-log.json', 'w') as npc_error_log:
                        json.dump(npc_error_log_new, npc_error_log, indent=2)
                try:
                    conn = sqlite3.connect(config.database)
                    c = conn.cursor()
                    c.execute("""SELECT npc_id FROM npc_master WHERE npc_name = ?""", (npc_name,))
                    npc_id = c.fetchone()[0];
                    if not npc_id:
                        print('NPC not found, aborting parse for now...')
                        return
                    for zone_name in npc_object['Zone']:
                        zone_id = None
                        # This may look like bad code smell, but this pre-SELECT is here to avoid constraints which were autoincrementing 'zone_master.zone_id' unnecessarily
                        c.execute("""SELECT zone_id FROM zone_master WHERE zone_name = ?""", (zone_name,))
                        zone_id = c.fetchone()
                        if zone_id:
                            zone_id = zone_id[0]
                        else:
                            c.execute("""INSERT OR IGNORE INTO zone_master (zone_name) VALUES (?)""", (zone_name,))
                            c.execute("""SELECT zone_id FROM zone_master WHERE zone_name = ?""", (zone_name,))
                            new_zone_result = c.fetchone()
                            if new_zone_result:
                                zone_id = new_zone_result[0]
                        if zone_id:
                            c.execute("""INSERT INTO npc_zone (zone_id, npc_id) VALUES (?, ?)""", (zone_id, npc_id))
                    conn.commit()
                    conn.close()

                    with open('./data/latest_npc_zone_parse.json', 'w') as latest_parse_json:
                        json.dump([{npc_name: npc_url}], latest_parse_json, indent=2)
                    return npc_object
                except sqlite3.Error as e:
                    print(f'SQLite error: {e}')
                except Exception as e:
                    print(f'An error occurred: {e}')
            else:
                print(f'Failed to retrieve data fom {npc_url}')
                return None 
 
async def npc_zone_scrape():
    with open('./data/npc_urls.json', 'r') as npc_urls:
        data = json.load(npc_urls)
    with open('./data/latest_npc_zone_parse.json', 'r') as latest_parse_json:
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
                return await npc_zone_data_scrape(npc)
            
        tasks = [limited_task(npc) for npc in data]
        results = await asyncio.gather(*tasks)

        for result in results:
            if result:
                print(result)
     
if __name__ == "__main__":
    asyncio.run(npc_zone_scrape())

