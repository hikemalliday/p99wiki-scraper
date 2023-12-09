from bs4 import BeautifulSoup
import re
import json
import requests
import omit
import math

base_url = 'https://wiki.project1999.com'

convert_to_none = ["()", "?", "??", "???", "????", "Various", "Multiple", "Description needed.", "Triggered"]

def get_npc_race(soup: BeautifulSoup) -> str or None:
    race_element = soup.find('b', string='Race:')
    if race_element:
        race_string = race_element.find_next_sibling(string=True).strip()
        if race_string and race_string not in convert_to_none:
            return race_string
    return None

def get_npc_class(soup: BeautifulSoup) -> str or None:
    class_element = soup.find('b', string='Class:')
    return (
        class_element.find_next_sibling('a').text.strip()
        if class_element and class_element.find_next_sibling('a')
        else None
    )

# TODO: Refactor the level that is returned: Average, min, max?
def get_npc_level(soup: BeautifulSoup) -> list:
    level_element = soup.find('b', string='Level:')
    if level_element:
        level_string = level_element.find_next_sibling(string=True).strip()
        if level_string in convert_to_none:
            return [None]
        elif '-' in level_string:
            return level_string.split('-')
        else:
            return [level_string]
    return [None]

def get_npc_zone(soup: BeautifulSoup) -> list:
    zone_element = soup.find('b', string="Zone:")
    return (
        [', '.join([a.get_text(strip=True) for a in zone_element.find_parent('td').find_all('a')])]
        if zone_element
        else [None]
    )

def get_npc_respawn_time(soup: dict) -> str or None:
    respawn_time_element = soup.find('b', string="Respawn Time:")
    if respawn_time_element:
        respawn_time_string = respawn_time_element.find_next_sibling(string=True).strip()
        if respawn_time_string in convert_to_none:
            return None
        if respawn_time_string:
            respawn_time_array = respawn_time_string.split(' ')
            if len(respawn_time_array) > 1:
                respawn_time_array = [respawn_time_array[0] , respawn_time_array[1]]
                if respawn_time_array[1] == 'hours':
                    try:
                        respawn_time_string = math.floor(float(respawn_time_array[0][0]) * 60)
                    except ValueError: # Edge case. If we encounter a weird string, attempt to convert the first char in the string to a float.
                        respawn_time_float = float(respawn_time_array[0][0])
                elif respawn_time_array[1] == 'Days' or respawn_time_array[1] == 'days':
                    respawn_time_string = math.floor(float(respawn_time_array[0]) * 1440)
                elif respawn_time_array[1] == 'minutes' or respawn_time_array[1] == 'minutes,':
                    respawn_time_string = math.floor(float(respawn_time_array[0]))
            return respawn_time_string
    return None

def get_npc_location(soup: BeautifulSoup) -> str or None:
    # We will probably use regex and just return the first match, format: '(5754, -2024)'
    pass

def get_npc_ac(soup: BeautifulSoup) -> str or None:
    ac_element = soup.find('b', string="AC:")
    if ac_element:
        td_element = ac_element.find_parent('td')
        if td_element:
            ac_element_string = td_element.get_text(strip=True, separator=' ')
            ac_element_string = ac_element_string.replace('AC:','').strip()
        if ac_element_string in convert_to_none:
             return None
        return ac_element_string
    return None

def get_npc_hp(soup: BeautifulSoup) -> str or None:
    hp_element = soup.find('b', string="HP:")
    if hp_element:
        td_element = hp_element.find_parent('td')
        if td_element:
            hp_element_string = td_element.get_text(strip=True, separator=' ')
            match = re.search(r'(\d+)', hp_element_string)
            if match:
                return int(match.group())
    return None

def get_npc_dmg_per_hit(soup: BeautifulSoup) -> list:
    results = []
    dmg_per_hit_element = soup.find('b', string="Damage per hit:")
    if dmg_per_hit_element:
        dmg_per_hit_string = dmg_per_hit_element.find_next_sibling(string=True)
        if dmg_per_hit_string:
            dmg_per_hit_string = dmg_per_hit_string.strip()
            dmg_per_hit_string = re.sub(r'[^-\d]', '', dmg_per_hit_string)
            results = [result.strip() for result in dmg_per_hit_string.split('-')]
            if len(results) == 1:
                results = [results[0], results[0]]
            return results
    return [None]

def get_npc_attacks_per_round(soup: BeautifulSoup) -> str or None:
    npc_attacks_per_round_element = soup.find('b', string="Attacks per round:")
    if npc_attacks_per_round_element:
        td_element = npc_attacks_per_round_element.find_parent('td')
        if td_element:
            npc_attacks_per_round_string = td_element.get_text(strip=True, separator=' ')
            npc_attacks_per_round_string = npc_attacks_per_round_string.replace("Attacks per round:", '')
            match = re.search(r'(\d+)', npc_attacks_per_round_string)
            if match and match not in convert_to_none:
                return int(match.group())
    return None

def get_npc_description(soup: BeautifulSoup) -> str or None:
    npc_description_element = soup.find('span', string=' Description ')
    if npc_description_element:
        npc_description_string = npc_description_element.find_next('p').text
        if npc_description_string.strip() not in convert_to_none:
            return npc_description_string
    return None

def get_npc_special(soup: BeautifulSoup) -> list:
    results = []
    npc_special_element = soup.find('b', string="Special:")
    if npc_special_element:
        td_element = npc_special_element.find_parent('td')
        if td_element:
            npc_special_string = td_element.get_text(strip=True, separator=' ')
            npc_special_string = npc_special_string.replace("Special:", '').strip()
            results = [result.strip() for result in npc_special_string.split(',')]
            if len(results) == 1 and results[0] in convert_to_none:
                return [None]
        return results
    return [None]
# TODO: Need 'None' handling, otherwise it skips too far ahead
def get_npc_items_drop(soup: BeautifulSoup) -> list:
    results = []
    npc_items_drop_element = soup.find('span', string=' Known Loot ')
    if npc_items_drop_element:
        ul_element = npc_items_drop_element.find_next('ul')
        if ul_element:
            li_elements = ul_element.find_all('li')
            for li_element in li_elements:
                if li_element.get_text(strip=True) == "None":
                    return [None]
                item_name = li_element.find_next('a').text
                results.append(item_name)
            return results
    return [None]
#TODO: Need 'None' handling, otherwise it skips too far ahead         
def get_npc_items_sold(soup: BeautifulSoup) -> list:            
    results = []
    npc_items_sold_element = soup.find('span', string=' Known Loot ')
    if npc_items_sold_element:
        ul_element = npc_items_sold_element.find_next('ul')
        if ul_element:
            li_elements = ul_element.find_all('li')
            for li_element in li_elements:
                if li_element.get_text(strip=True) == "None":
                    return [None]
                item_name = li_element.find_next('a').text
                results.append(item_name)
            return results
    return [None]
    
# TODO: Refactor
# Return a dict here, so we can also return 
def get_npc_factions(soup: BeautifulSoup) -> list:
    results = []
    npc_factions_element = soup.find('span', string=' Factions ')
    if npc_factions_element:
        ul_element = npc_factions_element.find_next('ul')
        if ul_element:
            #print('debug 1')
            li_elements = ul_element.find_all('li')
            #print('debug 2')
            for li_element in li_elements:
                faction_hit = None
                #print('debug 3')
                # Need to check for a None first.
                #print(li_element.text)
                if li_element.get_text(strip=True) == "None":
                    #print('conditional debug')
                    faction_name = None
                else:
                    faction_name = li_element.find_next('a').text.replace("(Faction)", '')
                    
                    faction_hit = li_element.find_next('a').find_next('span')
                    if faction_hit:
                        #print('debug 4')
                        faction_hit = faction_hit.text.replace('(', '').replace(')', '')
                        if faction_hit in convert_to_none:
                            faction_hit = None
                results.append([faction_name, faction_hit])
                #print('debug 5')
            return results  
        return [None, None]
            
# TODO: Refactor
def get_npc_opposing_factions(soup: BeautifulSoup) -> list:
    results = []
    npc_opposing_factions_element = soup.find('span', string=' Factions ')
    if npc_opposing_factions_element:
        ul_element = npc_opposing_factions_element.find_next('ul')
        if ul_element:
            # print('debug 1')
            li_elements = ul_element.find_all('li')
            # print('debug 2')
            for li_element in li_elements:
                faction_hit = None
                # print('debug 3')
                # Need to check for a None first.
                if li_element.get_text(strip=True) == "None":
                    # print('conditional debug')
                    faction_name = None
                else:
                    faction_name = li_element.find_next('a').text.replace("(Faction)", '')
                    faction_hit = li_element.find_next('a').find_next('span')
                    if faction_hit:
                        # print('debug 4')
                        faction_hit = faction_hit.text.replace('(', '').replace(')', '')
                        if faction_hit in convert_to_none:
                            faction_hit = None
                results.append([faction_name, faction_hit])
                # print('debug 5')
            return results  
        return [None, None]

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
                npc_object[name.text] = base_url + '/' + name.text.replace(' ', '_').replace("`", '%60')
                npcs_list.append(npc_object)
                npc_object = {}
            next_link = soup.find('a', string='next 200')
            if next_link:
                next_url = base_url + next_link.get('href')
                print('Next URL:', next_url)
            else:
                print("Next page not found, ending loop.")
                break
        else:
            print(f'Error: Unable to fetch the webpage. Status code: {response.status_code}')
    print('Scraping complete, calling "create_npc_urls_json()"...')
    create_npc_urls_json(npcs_list)

def npc_data_scrape():
    counter = 0
    with open("./data/npc_urls.json", 'r') as npc_urls:
        data = json.load(npc_urls)
        for npc in data:
            npc_name = list(npc.keys())[0]
            npc_url = npc[npc_name]
            print(f"NPC Name: {npc_name}, NPC URL: {npc_url}")
            response = requests.get(npc_url, verify =False)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                print('get_npc_race(): ' + str(get_npc_race(soup)))
                print('get_npc_class(): ' + str(get_npc_class(soup)))
                print('get_npc_level(): ' + str(get_npc_level(soup)))
                print('get_npc_zone(): ' + str(get_npc_zone(soup)))
                print('get_npc_respawn_time(): ' + str(get_npc_respawn_time(soup)))
                print('get_npc_ac(): ' + str(get_npc_ac(soup)))
                print('get_npc_hp():' + str(get_npc_hp(soup)))
                print('get_npc_dmg_per_hit():' + str(get_npc_dmg_per_hit(soup)))
                print('get_npc_attacks_per_round():' + str(get_npc_attacks_per_round(soup)))
                print('get_npc_special(): ' + str(get_npc_special(soup)))
                print('get_npc_description(): ' + str(get_npc_description(soup)))
                print('get_npc_items_drop(): ' + str(get_npc_items_drop(soup)))
                print('get_npc_factions(): ' + str(get_npc_factions(soup)))
                print('get_npc_opposing_factions(): ' + str(get_npc_opposing_factions(soup)))
            counter += 1
            print(counter)
    print(counter)

def npc_debug_scrape(npc_url: str):
    response = requests.get(npc_url, verify = False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        print('get_npc_race(): ' + str(get_npc_race(soup)))
        print('get_npc_class(): ' + str(get_npc_class(soup)))
        print('get_npc_level(): ' + str(get_npc_level(soup)))
        print('get_npc_zone(): ' + str(get_npc_zone(soup)))
        print('get_npc_respawn_time(): ', str(get_npc_respawn_time(soup)))
        print('get_npc_ac(): ' + str(get_npc_ac(soup)))
        print('get_npc_hp(): ' + str(get_npc_hp(soup)))
        print('get_npc_dmg_per_hit(): ' + str(get_npc_dmg_per_hit(soup)))
        print('get_npc_attacks_per_round(): ' + str(get_npc_attacks_per_round(soup)))
        print('get_npc_special(): ' + str(get_npc_special(soup)))
        print('get_npc_description(): ' + str(get_npc_description(soup)))
        print('get_npc_items_drop(): ' + str(get_npc_items_drop(soup)))
        print('get_npc_factions(): ' + str(get_npc_factions(soup)))
        print('get_npc_opposing_factions(): ' + str(get_npc_opposing_factions(soup)))