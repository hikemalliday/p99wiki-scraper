from bs4 import BeautifulSoup
import json
import requests
import omit
import sqlite3
import config
import parse_functions

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

def npc_master_scrape():
    counter = 0
    with open("./data/npc_urls.json", 'r') as npc_urls:
        master_error_list = []
        data = json.load(npc_urls)
        for npc in data:
            try:
                errors = None
                npc_name = list(npc.keys())[0]
                npc_url = npc[npc_name]
                print(f"NPC Name: {npc_name}, NPC URL: {npc_url}")
                response = requests.get(npc_url, verify =False)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    npc_object = {
                    "Name": npc_name,
                    "Description": parse_functions.get_npc_description(soup),
                    "Race": parse_functions.get_npc_race(soup),
                    "Class": parse_functions.get_npc_class(soup),
                    "Level": parse_functions.get_npc_level(soup),
                    "Respawn": parse_functions.get_npc_respawn_time(soup),
                    "AC": parse_functions.get_npc_ac(soup),
                    "HP": parse_functions.get_npc_hp(soup),
                    "Damage per hit": parse_functions.get_npc_dmg_per_hit(soup),
                    "Attacks per round": parse_functions.get_npc_attacks_per_round(soup),  
                }
                    for key, value in npc_object.items():
                        if value == 'Error':
                            if errors is None:
                                errors = {npc_name: {}}
                            errors[npc_name][key] = npc_url
                    if errors:
                        master_error_list.append(errors)

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
            except Exception as e:
                print(f"Error scraping NPC {npc_name}: {e}")
            counter += 1
            print(counter)
    print(counter)

    npc_url_scrape()
    npc_master_scrape()







