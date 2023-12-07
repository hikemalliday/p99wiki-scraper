from bs4 import BeautifulSoup
import requests

ommit_these_elements = [
'previous 200',
'Disclaimer',
'Create new user',
'Wiki markup help',
'Install P99',
'navigation',
'search',
'Merchants',
'Named Mobs',
'Raid Encounters',
'Category',
'Discussion',
'View source',
'History',
'Create account',
'Log in',
'https://wiki.project1999.com/Mobs_By_Level',
'http://web.archive.org/web/20021129210131/http://www.geocities.com/ficticiousname9/',
'https://wiki.project1999.com/index.php?title=Category:NPCs&oldid=328565',
'Main page',
'Zones',
'Quests',
'NPCs',
'Equipment',
'Armor Sets',
'Clickies',
'Resist Gear',
'Lore of Norrath',
'Languages',
'Deities',
'Factions',
'Guides',
'Game Mechanics',
'Races',
'Classes',
'Skills',
'Disciplines',
'Tradeskills',
'Cultural Tradeskills',
'Spells',
'Pet Guide',
'Haste Guide',
'Newbie Guide',
'Gear Reference',
'Player List from Live',
'Auction Price Tracker',
'Magelo (Blue)',
'Magelo (Red)',
'Magelo (Green)',
'Random Page',
'What links here',
'Related changes',
'Special pages',
'Printable version',
'Permanent link',
'Page information',
'Privacy policy',
'About Project 1999 Wiki',
'Disclaimers',
'next 200',
]

npc_links = {

}

next_url = ''
next_page = True
base_url = 'https://wiki.project1999.com'
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
            if name.text in ommit_these_elements:
                continue
            npc_links[name.text] = name.text.replace(' ', '_')
            print(npc_links[name.text])
        
        next_link = soup.find('a', string='next 200')
        if next_link:
            next_url = base_url + next_link.get('href')
            print('Next URL:', next_url)
        else:
            print("Next page not found, ending loop.")
            break
    else:
        print(f'Error: Unable to fetch the webpage. Status code: {response.status_code}')

print(npc_links)
    