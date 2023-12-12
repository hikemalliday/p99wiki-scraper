from bs4 import BeautifulSoup
import json
import requests
import sqlite3
import config
import parse_functions
import omit

def npc_faction_scrape():
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
                    "Factions": parse_functions.get_npc_factions(soup),
                    "Opposing factions": parse_functions.get_npc_opposing_factions(soup),
                }
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
                        # This may look like bad code smell, but this pre-SELECT is here to avoid constraints which were autoincrementing unnecessarily
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
                        # This may look like bad code smell, but this pre-SELECT is here to avoid constraints which were autoincrementing unnecessarily
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
                    
            except Exception as e:
                print(e)
                return e
            
npc_faction_scrape()