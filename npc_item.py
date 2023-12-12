from bs4 import BeautifulSoup
import json
import requests
import sqlite3
import config
import parse_functions
import omit

def npc_items_scrape():
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
                    "Items drop": parse_functions.get_npc_items_drop(soup),
                    "Items sold": parse_functions.get_npc_items_sold(soup)
                }
                    conn = sqlite3.connect(config.database)
                    c = conn.cursor()

                    print(npc_name)
                    c.execute("""SELECT npc_id FROM npc_master WHERE npc_name = ?""", (npc_name,))
                    npc_id = c.fetchone()[0];
                    if not npc_id:
                        print('NPC not found, aborting parse for now...')
                        return
                    print('npc_id:')
                    print(npc_id)
                    print('Items drop:')
                    print(npc_object['Items drop'])
                    print('Items sold')
                    print(npc_object['Items sold'])
                    # Items drop:
                    
                    for item_name in npc_object['Items drop']:
                        if any(item_name == keyword for keyword in omit.omit_these):
                            continue
                        item_id = None
                        # This may look like bad code smell, but this pre-SELECT is here to avoid constraints which were autoincrementing  unnecessarily
                        c.execute("""SELECT item_id FROM item_master WHERE item_name = ?""", (item_name,))
                        item_id = c.fetchone()
                        if item_id:
                            item_id = item_id[0]
                        else:
                            c.execute("""INSERT OR IGNORE INTO item_master (item_name) VALUES (?)""", (item_name,))
                            c.execute("""SELECT item_id FROM item_master WHERE item_name = ?""", (item_name,))
                            new_item_result = c.fetchone()
                            if new_item_result:
                                item_id = new_item_result[0]
                        if item_id:
                            c.execute("""INSERT INTO npc_loot (item_id, npc_id) VALUES (?, ?)""", (item_id, npc_id))

                    # Items sold:
                    for item_name in npc_object['Items sold']:
                        if any(item_name == keyword for keyword in omit.omit_these):
                            continue
                        item_id = None
                        # This may look like bad code smell, but this pre-SELECT is here to avoid constraints which were autoincrementing  unnecessarily
                        c.execute("""SELECT item_id FROM item_master WHERE item_name = ?""", (item_name,))
                        item_id = c.fetchone()
                        if item_id:
                            item_id = item_id[0]
                        else:
                            c.execute("""INSERT OR IGNORE INTO item_master (item_name) VALUES (?)""", (item_name,))
                            c.execute("""SELECT item_id FROM item_master WHERE item_name = ?""", (item_name,))
                            new_item_result = c.fetchone()
                            if new_item_result:
                                item_id = new_item_result[0]
                        if item_id:
                            c.execute("""INSERT INTO npc_sold (item_id, npc_id) VALUES (?, ?)""", (item_id, npc_id))

                    
                    conn.commit()
                    conn.close()
                    
            except Exception as e:
                print(e)
                return e
            