from bs4 import BeautifulSoup
import re
import omit
import requests
import config
import os
              
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

def get_npc_level(soup: BeautifulSoup) -> list:
    try:
        level_element = soup.find('b', string='Level:')
        if level_element:
            level_string = level_element.find_next_sibling(string=True).strip()
            match = re.search(r'\d+', level_string)
            if match:
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
            
def get_item_hp(soup: BeautifulSoup) -> int or str or None:
    try:
        hp_container = soup.find('div', class_='itemicon')
        if hp_container:
            hp_string = hp_container.find_next('p').text
            if hp_string:
                hp_match = re.search(r'\bHP:\s*([+-]?\d+)', hp_string)
                if hp_match:
                    hp = hp_match.group(1)
                    #print('HP: ' + str(hp))
                    return int(hp)
        else:
            return None
    except Exception as e:
        print(e)
        return 'Error'
    
def get_item_mp(soup: BeautifulSoup) -> int or str or None:
    try:
        mp_container = soup.find('div', class_='itemicon')
        if mp_container:
            mp_string = mp_container.find_next('p').text
            if mp_string:
                mp_match = re.search(r'\bMANA:\s*([+-]?\d+)', mp_string)
                if mp_match:
                    mp = mp_match.group(1)
                    #print('MANA: ' + str(mp))
                    return int(mp)
        else:
            return None
    except Exception as e:
        print(e)
        return 'Error'
    
def get_item_str(soup: BeautifulSoup) -> int or str or None:
    try:
        str_container = soup.find('div', class_='itemicon')
        if str_container:
            str_string = str_container.find_next('p').text
            if str_string:
                str_match = re.search(r'\bSTR:\s*([+-]?\d+)', str_string)
                if str_match:
                    strength = str_match.group(1)
                    #print('STR: ' + str(strength))
                    return int(strength)
        else:
            return None
    except Exception as e:
        print(e)
        return 'Error'
    
def get_item_sta(soup: BeautifulSoup) -> int or str or None:
    try:
        sta_container = soup.find('div', class_='itemicon')
        if sta_container:
            sta_string = sta_container.find_next('p').text
            if sta_string:
                sta_match = re.search(r'\bSTA:\s*([+-]?\d+)', sta_string)
                if sta_match:
                    sta = sta_match.group(1)
                    #print('STA: ' + str(sta))
                    return int(sta)
        else:
            return None
    except Exception as e:
        print(e)
        return 'Error'
    
def get_item_dex(soup: BeautifulSoup) -> int or str or None:
    try:
        dex_container = soup.find('div', class_='itemicon')
        if dex_container:
            dex_string = dex_container.find_next('p').text
            if dex_string:
                dex_match = re.search(r'\bDEX:\s*([+-]?\d+)', dex_string)
                if dex_match:
                    dex = dex_match.group(1)
                    #print('DEX: ' + str(dex))
                    return int(dex)
        else:
            return None
    except Exception as e:
        print(e)
        return 'Error'
    
def get_item_agi(soup: BeautifulSoup) -> int or str or None:
    try:
        agi_container = soup.find('div', class_='itemicon')
        if agi_container:
            agi_string = agi_container.find_next('p').text
            if agi_string:
                agi_match = re.search(r'\bDEX:\s*([+-]?\d+)', agi_string)
                if agi_match:
                    agi = agi_match.group(1)
                    #print('AGI: ' + str(agi))
                    return int(agi)
        else:
            return None
    except Exception as e:
        print(e)
        return 'Error'
    
def get_item_wis(soup: BeautifulSoup) -> int or str or None:
    try:
        wis_container = soup.find('div', class_='itemicon')
        if wis_container:
            wis_string = wis_container.find_next('p').text
            if wis_string:
                wis_match = re.search(r'\bWIS:\s*([+-]?\d+)', wis_string)
                if wis_match:
                    wis = wis_match.group(1)
                    #print('WIS: ' + str(wis))
                    return int(wis)
        else:
            return None
    except Exception as e:
        print(e)
        return 'Error'
    
def get_item_int(soup: BeautifulSoup) -> int or str or None:
    try:
        int_container = soup.find('div', class_='itemicon')
        if int_container:
            int_string = int_container.find_next('p').text
            if int_string:
                int_match = re.search(r'\bINT:\s*([+-]?\d+)', int_string)
                if int_match:
                    intelligence = int_match.group(1)
                    #print('MP: ' + str(intelligence))
                    return int(intelligence)
        else:
            return None
    except Exception as e:
        print(e)
        return 'Error'
    
def get_item_cha(soup: BeautifulSoup) -> int or str or None:
    try:
        cha_container = soup.find('div', class_='itemicon')
        if cha_container:
            cha_string = cha_container.find_next('p').text
            if cha_string:
                cha_match = re.search(r'\bCHA:\s*([+-]?\d+)', cha_string)
                if cha_match:
                    cha = cha_match.group(1)
                    #print('CHA: ' + str(cha))
                    return int(cha)
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
                    print('TEST')
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
        
