from bs4 import BeautifulSoup
import re
import omit
import requests
import config
import os

debug = False
              
def get_npc_race(soup: BeautifulSoup) -> str or None:
    try:
        race_element = soup.find('b', string='Race:')
        if race_element:
            race_string = race_element.find_next_sibling(string=True).strip()
            if race_string and race_string not in omit.convert_to_none:
                if debug == True:
                    print(race_string)
                return race_string
        return None
    except:
        return 'Error'
# TODO: consider refactoring this
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

def get_npc_level(soup: BeautifulSoup) -> list:
    try:
        level_element = soup.find('b', string='Level:')
        if level_element:
            level_string = level_element.find_next_sibling(string=True).strip()
            match = re.search(r'\d+', level_string)
            if match:
                level_array = re.split(r'[-,]', level_string)
                if debug == True:
                    print(level_array)
                if len(level_array) > 1:
                    return [level_array[0].strip(), level_array[1].strip()]
                else:
                    return [level_array[0].strip(), level_array[0].strip()]
        return [None, None]
    except Exception as e:
        return ['Error', 'Error']
# TODO: consider refactoring this
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
                if debug == True:
                    print(respawn_time_digits)
                respawn_time_digits = matches.group(1)
                return int(respawn_time_digits) * multiplier 
        return None
    except:
        return 'Error'

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
            if debug == True:
                print(ac_element_string)
            return int(ac_element_string)
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
                    if debug == True:
                        print(match.group())
                    return int(match.group())
        return None
    except:
        return 'Error'
#TODO: refactor 
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
                if debug == True:
                    print(results)              
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
                    if debug == True:
                        print(match.group())
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
                if debug == True:
                    print(npc_description_string)
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
            if debug == True:
                print(results)
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
                if debug == True:
                    print(results)
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
                if debug == True:
                    print(results)
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
                if debug == True:
                    print(results)
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
                if debug == True:
                    print(results)
                return results  
            return [None]
    except:
        return ['Error']

def get_npc_master_object(soup: BeautifulSoup, npc_name: str):
    npc_object = {
        "Name": npc_name,
        "Description": get_npc_description(soup),
        "Race": get_npc_race(soup),
        "Class": get_npc_class(soup),
        "Level": get_npc_level(soup),
        "Respawn": get_npc_respawn_time(soup),
        "AC": get_npc_ac(soup),
        "HP": get_npc_hp(soup),
        "Damage per hit": get_npc_dmg_per_hit(soup),
        "Attacks per round": get_npc_attacks_per_round(soup)
    }
    return npc_object

def get_item_properties(soup: BeautifulSoup) -> list:
    properties = ['EXPENDABLE', 'MAGIC ITEM', 'LORE ITEM', 'NO DROP', 'QUEST ITEM', 'NO RENT']
    try:
        properties_container = soup.find('div', class_='itemicon')
        if properties_container:
            properties_string = properties_container.find_next('p').text
            if properties_string:
                results = [property for property in properties if property in properties_string]
                #print('properties: ' + str(results))
                if results == []:
                    return ['None']
                else:
                    return results          
        else:
            return [None]
    except Exception as e:
        print(e)
        return ['Error']
    
def get_item_slot(soup: BeautifulSoup) -> list:
    slots = [
            'PRIMARY', 
             'SECONDARY', 
             'RANGE', 
             'ARMS', 
             'BACK', 
             'CHEST', 
             'EAR', 
             'FACE', 
             'FEET', 
             'FINGERS', 
             'HANDS', 
             'HEAD', 
             'LEGS', 
             'NECK', 
             'SHOULDERS', 
             'WAIST', 
             'WRIST', 
             'AMMO'
             ]
    try:
        slots_container = soup.find('div', class_='itemicon')
        if slots_container:
            slots_string = slots_container.find_next('p').text
            if slots_string:
                results = [slot for slot in slots if slot in slots_string]
                if results == []:
                    results = ['None']
                #print('slots: ' + str(results))
                return results
        else:
            return [None]
    except Exception as e:
        print(e)
        return ['Error']
    
def get_item_class(soup: BeautifulSoup) -> list:
    classes = ['ENC', 'MAG', 'NEC', 'WIZ', 'CLR', 'DRU', 'SHM', 'BRD', 'MNK', 'RNG', 'ROG', 'PAL', 'SHD', 'WAR']
    results = []
    try:
        classes_container = soup.find('div', class_='itemicon')
        if classes_container:
            classes_string = classes_container.find_next('p').text
            if classes_string:
                classes_match = re.search(r'Class: (.+)', classes_string)
                if classes_match:
                    class_info = classes_match.group(1)
                    results = [class_name for class_name in classes if class_name in classes]
                    if class_info == 'All':
                        results = classes
                    #print('class info: ' + str(results))
                    return results
        else:
            return [None]
    except Exception as e:
        print(e)
        return ['Error']

def get_item_race(soup: BeautifulSoup) -> list:
    races = ['BAR', 'DEF', 'DWF', 'ERU', 'GNM', 'HEF', 'HFL', 'HIE', 'HUM', 'IKS', 'OGR', 'TRL', 'ELF']
    results = []
    try:
        races_container = soup.find('div', class_='itemicon')
        if races_container:
            races_string = races_container.find_next('p').text
            if races_string:
                races_match = re.search(r'Class: (.+)', races_string)
                if races_match:
                    class_info = races_match.group(1)
                    results = [class_name for class_name in races if class_name in races]
                    if class_info == 'All':
                        results = races
                    #print('race info: ' + str(results))
                    return results
        else:
            return [None]
    except Exception as e:
        print(e)
        return ['Error']
    
def get_item_dmg(soup: BeautifulSoup) -> int or str or None:
    try:
        damage_container = soup.find('div', class_='itemicon')
        if damage_container:
            damage_string = damage_container.find_next('p').text
            if damage_string:
                dmg_match = re.search(r'DMG:\s*(\d+)', damage_string)
                if dmg_match:
                    dmg = dmg_match.group(1)
                    #print('dmg: ' + str(dmg))
                    return dmg
        else:
            return None
    except Exception as e:
        print(e)
        return 'Error'
    
def get_item_delay(soup: BeautifulSoup) -> int or str or None:
    try:
        atk_delay_container = soup.find('div', class_='itemicon')
        if atk_delay_container:
            atk_delay_string = atk_delay_container.find_next('p').text
            if atk_delay_string:
                atk_delay_match = re.search(r'Atk Delay:\s*(\d+)', atk_delay_string)
                if atk_delay_match:
                    delay = atk_delay_match.group(1)
                    #print('delay: ' + str(delay))
                    return delay
        else:
            return None
    except Exception as e:
        print(e)
        return 'Error'
    
def get_item_ac(soup: BeautifulSoup) -> int or str or None:
    try:
        ac_container = soup.find('div', class_='itemicon')
        if ac_container:
            ac_string = ac_container.find_next('p').text
            if ac_string:
                ac_match = re.search(r'AC:\s*(\d+)', ac_string)
                if ac_match:
                    ac = ac_match.group(1)
                    #print('AC: ' + str(ac))
                    return ac
        else:
            return None
    except Exception as e:
        print(e)
        return 'Error'
    
def get_item_ac(soup: BeautifulSoup) -> int or str or None:
    try:
        ac_container = soup.find('div', class_='itemicon')
        if ac_container:
            ac_string = ac_container.find_next('p').text
            if ac_string:
                ac_match = re.search(r'AC:\s*(\d+)', ac_string)
                if ac_match:
                    ac = ac_match.group(1)
                    #print('AC: ' + str(ac))
                    return ac
        else:
            return None
    except Exception as e:
        print(e)
        return 'Error'
    
def get_item_effect(soup: BeautifulSoup) -> str or None:
    try:
        effect_container = soup.find('div', class_='itemicon')
        if effect_container:
            effect_string = effect_container.find_next('p').text
            if effect_string and 'Effect:' in effect_string:
                effect = effect_container.find_next('a').text
                if effect:
                    #print('Effect: ' + str(effect))
                    return effect
        else:
            return None
    except Exception as e:
        print(e)
        return 'Error'
             
def get_item_resists(soup: BeautifulSoup, resist_type: str) -> int or str or None:
    try:
        resist_container = soup.find('div', class_='itemicon')
        if resist_container:
            resist_string = resist_container.find_next('p').text
            if resist_string:
                resist_match = re.search(r'\b' + re.escape(resist_type) + r':\s*([+-]?\d+)', resist_string)
                if resist_match:
                    resist = resist_match.group(1)
                    #print(f'{resist_type}: ' + str(resist))
                    return int(resist)
        else:
            return None
    except Exception as e:
        print(e)
        return 'Error'
    
def get_item_wt(soup: BeautifulSoup) -> int or str or None:
    try:
        wt_container = soup.find('div', class_='itemicon')
        if wt_container:
            wt_string = wt_container.find_next('p').text
            if wt_string:
                wt_match = re.search(r'\bWT:\s*([+-]?\d+(?:\.\d+)?)', wt_string)
                if wt_match:
                    wt = wt_match.group(1)
                    #print('WT: ' + str(wt))
                    return float(wt)
        else:
            return None
    except Exception as e:
        print(e)
        return 'Error'
    
def get_item_size(soup: BeautifulSoup) -> str or None:
    try:
        size_container = soup.find('div', class_='itemicon')
        if size_container:
            size_string = size_container.find_next('p').text
            if size_string:
                size_match = re.search(r'Size:\s*(\w+)', size_string)
                if size_match:
                    size = size_match.group(1)
                    #print('SIZE: ' + str(size))
                    return size
        else:
            return None
    except Exception as e:
        print(e)
        return 'Error'

def get_item_img(soup: BeautifulSoup) -> str:
    try:
        item_container = soup.find('div', class_='floatright')
        if item_container:
            image_container = item_container.find_next('img')
            if image_container:
                img_url = image_container.get('src')
                if not os.path.exists(f'.{img_url}'):
                    response = requests.get(f'{config.base_url}{img_url}', verify=False)
                    if response.status_code == 200:
                        with open(f'./{img_url}', 'wb') as image:
                            image.write(response.content)
                            print('Image saved.')
                            print(img_url)
                            return str(img_url)
                else:
                    return str(img_url)      
        else:
            return 'Error'
    except Exception as e:
        print(e)
        return 'Error'
        
def get_item_stat(soup: BeautifulSoup, stat_type: str) -> int or str or None:
    try:
        stat_container = soup.find('div', class_='itemicon')
        if stat_container:
            stat_string = stat_container.find_next('p').text
            if stat_string:
                stat_match = re.search(r'\b' + re.escape(stat_type) + r':\s*([+-]?\d+)', stat_string)
                if stat_match:
                    stat = stat_match.group(1)
                    if debug == True:
                        print(stat)
                        return 'Error'
                    #print(f'{stat_type}: ' + str(stat))
                    return int(stat)
        else:
            return None
    except Exception as e:
        print(e)
        return 'Error'
    
def get_item_object(soup: BeautifulSoup, item_name: str):
    item_object = {
            "Item Name": item_name,
            "Properties": get_item_properties(soup),
            "Slots": get_item_slot(soup),
            "Class": get_item_class(soup),
            "Race": get_item_race(soup),
            "DMG": get_item_dmg(soup),
            "Atk Delay": get_item_delay(soup),
            "AC": get_item_ac(soup),
            "Effect": get_item_effect(soup),
            "HP": get_item_stat(soup, 'HP'),
            "MP": get_item_stat(soup, 'MANA'),
            "STR": get_item_stat(soup, 'STR'),
            "STA": get_item_stat(soup, 'STA'),
            "DEX": get_item_stat(soup, 'DEX'),
            "AGI": get_item_stat(soup, 'AGI'),
            "WIS": get_item_stat(soup, 'WIS'),
            "INT": get_item_stat(soup, 'INT'),
            "CHA": get_item_stat(soup, 'CHA'),
            "SV_FIRE": get_item_resists(soup, 'SV_FIRE'),
            "SV_DISEASE": get_item_resists(soup, 'SV_DISEASE'),
            "SV_COLD": get_item_resists(soup, 'SV_COLD'),
            "SV_MAGIC": get_item_resists(soup, 'SV_MAGIC'),
            "SV_POISON": get_item_resists(soup, 'SV_POISON'),
            "WT": get_item_wt(soup),
            "Size": get_item_size(soup),
            "Item Image": get_item_img(soup)
            }
    return item_object


    pass