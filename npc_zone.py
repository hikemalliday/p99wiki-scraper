from bs4 import BeautifulSoup
import json
import requests
import sqlite3
import config
import parse_functions

def npc_zone_scrape():
    with open("./data/npc_urls.json", 'r') as npc_urls:
        data = json.load(npc_urls)
        for npc in data:
            try:
                npc_name = list(npc.keys())[0]
                npc_url = npc[npc_name]
                response = requests.get(npc_url, verify =False)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    npc_object = {
                    "Zone": parse_functions.get_npc_zone(soup),
                }
                    conn = sqlite3.connect(config.database)
                    c = conn.cursor()

                    print(npc_name)
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
                    
            except Exception as e:
                print(e)
                return e
