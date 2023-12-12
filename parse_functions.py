from bs4 import BeautifulSoup
import re
import omit

def get_npc_race(soup: BeautifulSoup) -> str or None:
    try:
        race_element = soup.find('b', string='Race:')
        if race_element:
            race_string = race_element.find_next_sibling(string=True).strip()
            if race_string and race_string not in omit.convert_to_none:
                return race_string
        return None
    except:
        return 'Error'

def get_npc_class(soup: BeautifulSoup) -> str or None:
    try:
        class_element = soup.find('b', string='Class:')
        return (
            class_element.find_next_sibling('a').text.strip()
            if class_element and class_element.find_next_sibling('a')
            else None
        )
    except:
        return 'Error'

# TODO: Refactor the level that is returned: Average, min, max?
# BAD CODE SMELL
def get_npc_level(soup: BeautifulSoup) -> list:
    try:
        print('test1')
        level_element = soup.find('b', string='Level:')
        if level_element:
            print('test2')
            level_string = level_element.find_next_sibling(string=True).strip()
            match = re.search(r'\d+', level_string)
            print('test3')
            if match:
                # level_digits = int(match.group())
                level_array = re.split(r'[-,]', level_string)
                print(level_array)
                if len(level_array) > 1:
                    return [level_array[0].strip(), level_array[1].strip()]
                else:
                    return [level_array[0].strip(), level_array[0].strip()]
        return [None, None]
    except Exception as e:
        return ['Error', 'Error']

def get_npc_zone(soup: BeautifulSoup) -> list:
    try:
        zone_element = soup.find('b', string="Zone:")
        zones = [a.get_text(strip=True) for a in zone_element.find_parent('td').find_all('a')]
        return (
            zones[0].split(',') if ',' in zones[0] else zones
        ) if zone_element else [None]
    except:
        return ['Error']

# TODO: Refactor. add string check, then take the first char in string.
def get_npc_respawn_time(soup: BeautifulSoup) -> int or None or str:
    try:
        multiplier = 1
        respawn_time_element = soup.find('b', string="Respawn Time:")
        if respawn_time_element:
            respawn_time_string = respawn_time_element.find_next_sibling(string=True)
            if respawn_time_string:
                if any(keyword in respawn_time_string for keyword in ["day", "days", "Day", "Days"]):
                    multiplier = 1440
                elif any(keyword in respawn_time_string for keyword in ["hour", "hours", "Hour", "Hours"]):
                    multiplier = 60
            matches = re.match(r'\D*(\d+)', respawn_time_string)
            if matches:
                respawn_time_digits = matches.group(1)
                return int(respawn_time_digits) * multiplier 
        return None
    except:
        return 'Error'

# TODO: Remove this, probably
def get_npc_location(soup: BeautifulSoup) -> str or None:
    # We will probably use regex and just return the first match, format: '(5754, -2024)'
    pass

def get_npc_ac(soup: BeautifulSoup) -> int or None:
    try:
        ac_element = soup.find('b', string="AC:")
        if ac_element:
            td_element = ac_element.find_parent('td')
            if td_element:
                ac_element_string = td_element.get_text(strip=True, separator=' ')
                ac_element_string = ac_element_string.replace('AC:','').strip()
            if ac_element_string in omit.convert_to_none:
                return None
            return ac_element_string
        return None
    except:
        return 'Error'

def get_npc_hp(soup: BeautifulSoup) -> str or None:
    try:
        k_flag = False
        hp_element = soup.find('b', string="HP:")
        if hp_element:
            td_element = hp_element.find_parent('td')
            if td_element:
                hp_element_string = td_element.get_text(strip=True, separator=' ')
                if 'k' in hp_element_string:
                    k_flag = True
                match = re.search(r'(\d+)', hp_element_string)
                if k_flag:
                    return int(match.group()) * 1000
                if match:
                    return int(match.group())
        return None
    except:
        return 'Error'
    
def get_npc_dmg_per_hit(soup: BeautifulSoup) -> list:
    try:
        results = []
        dmg_per_hit_element = soup.find('b', string="Damage per hit:")
        if dmg_per_hit_element:
            dmg_per_hit_string = dmg_per_hit_element.find_next_sibling(string=True)
            if dmg_per_hit_string:              
                if any(keyword in dmg_per_hit_string for keyword in omit.convert_to_none):                  
                    return [None, None]               
                dmg_per_hit_string = dmg_per_hit_string.strip()              
                dmg_per_hit_string = re.sub(r'[^-\d]', '', dmg_per_hit_string)               
                results = [int(result.strip()) for result in dmg_per_hit_string.split('-')]              
                if len(results) == 1:                   
                    results = [results[0], results[0]]               
                return results       
        return [None, None]
    except:
        return ['Error', 'Error']

def get_npc_attacks_per_round(soup: BeautifulSoup) -> str or None:
    try:
        npc_attacks_per_round_element = soup.find('b', string="Attacks per round:")
        if npc_attacks_per_round_element:
            td_element = npc_attacks_per_round_element.find_parent('td')
            if td_element:
                npc_attacks_per_round_string = td_element.get_text(strip=True, separator=' ')
                npc_attacks_per_round_string = npc_attacks_per_round_string.replace("Attacks per round:", '')
                match = re.search(r'(\d+)', npc_attacks_per_round_string)
                if match and match not in omit.convert_to_none:
                    return int(match.group())
        return None
    except:
        return 'Error'

def get_npc_description(soup: BeautifulSoup) -> str or None:
    try:
        npc_description_element = soup.find('span', string=' Description ')
        if npc_description_element:
            npc_description_string = npc_description_element.find_next('p').text
            if npc_description_string.strip() not in omit.convert_to_none:
                return npc_description_string
        return None
    except:
        return 'Error'

def get_npc_special(soup: BeautifulSoup) -> list:
    try:
        results = []
        npc_special_element = soup.find('b', string="Special:")
        if npc_special_element:
            td_element = npc_special_element.find_parent('td')
            if td_element:
                npc_special_string = td_element.get_text(strip=True, separator=' ')
                npc_special_string = npc_special_string.replace("Special:", '').strip()
                results = [result.strip() for result in npc_special_string.split(',')]
                if len(results) == 1 and results[0] in omit.convert_to_none:
                    return [None]
            return results
        return [None]
    except:
        return ['Error']

def get_npc_items_drop(soup: BeautifulSoup) -> list:
    try:
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
    except:
        return ['Error']
       
def get_npc_items_sold(soup: BeautifulSoup) -> list:
    try:            
        results = []
        npc_items_sold_element = soup.find('span', string=' Items Sold ')
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
    except:
        return ['Error']
    
# TODO: Refactor (bad code smell)
def get_npc_factions(soup: BeautifulSoup) -> list:
    try:
        results = []
        npc_factions_element = soup.find('span', string=' Factions ')
        if npc_factions_element:
            ul_element = npc_factions_element.find_next('ul')
            if ul_element:
                li_elements = ul_element.find_all('li')
                for li_element in li_elements:
                    faction_hit = None
                    if li_element.get_text(strip=True) == "None":
                        faction_name = None
                    else:
                        faction_name = li_element.find_next('a').text.replace("(Faction)", '').strip()
                        faction_hit = li_element.find_next('a').find_next('span')
                        if faction_hit:
                            faction_hit = faction_hit.text.replace('(', '').replace(')', '')
                            if faction_hit in omit.convert_to_none:
                                faction_hit = None
                    results.append([faction_name, faction_hit])
                return results  
            return [None]
    except:
        return ['Error']
            
# TODO: Refactor, bad code smell
def get_npc_opposing_factions(soup: BeautifulSoup) -> list:
    try:
        results = []
        npc_opposing_factions_element = soup.find('span', string=' Opposing Factions ')
        if npc_opposing_factions_element:
            ul_element = npc_opposing_factions_element.find_next('ul')
            if ul_element:
                li_elements = ul_element.find_all('li')
                for li_element in li_elements:
                    faction_hit = None
                    if li_element.get_text(strip=True) == "None":
                        faction_name = None
                    else:
                        faction_name = li_element.find_next('a').text.replace("(Faction)", '').strip()
                        faction_hit = li_element.find_next('a').find_next('span')
                        if faction_hit:
                            faction_hit = faction_hit.text.replace('(', '').replace(')', '')
                            if faction_hit in omit.convert_to_none:
                                faction_hit = None
                    results.append([faction_name, faction_hit])
                return results  
            return [None]
    except:
        return ['Error']
