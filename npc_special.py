from bs4 import BeautifulSoup
import json
import requests
import sqlite3
import config
import parse_functions

omit_these = ['None', None, '', 'Error', 'NULL']

def npc_special_scrape():
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
                    "Special": parse_functions.get_npc_special(soup),
                }
                    conn = sqlite3.connect(config.database)
                    c = conn.cursor()

                    print(npc_name)
                    c.execute("""SELECT npc_id FROM npc_master WHERE npc_name = ?""", (npc_name,))
                    npc_id = c.fetchone()[0];
                    if not npc_id:
                        print('NPC not found, aborting parse for now...')
                        return
                    for special_name in npc_object['Special']:
                        if any(special_name == value for value in omit_these):
                            continue
                        special_id = None
                        # This may look like bad code smell, but this pre-SELECT is here to avoid constraints which were autoincrementing unnecessarily
                        c.execute("""SELECT special_id FROM special_master WHERE special_name = ?""", (special_name,))
                        special_id = c.fetchone()
                        if special_id:
                            special_id = special_id[0]
                        else:
                            c.execute("""INSERT OR IGNORE INTO special_master (special_name) VALUES (?)""", (special_name,))
                            c.execute("""SELECT special_id FROM special_master WHERE special_name = ?""", (special_name,))
                            new_special_result = c.fetchone()
                            if new_special_result:
                                special_id = new_special_result[0]
                        if special_id:
                            c.execute("""INSERT INTO npc_special (special_id, npc_id) VALUES (?, ?)""", (special_id, npc_id))
                    conn.commit()
                    conn.close()
                    
            except Exception as e:
                print(e)
                return e