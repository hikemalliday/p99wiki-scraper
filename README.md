# p99wiki-scraper
###### A python based web scraping tool made to create a normalized database of https://wiki.project1999.com/Category:NPCs and https://wiki.project1999.com/Category:Items

This program scrapes the Project 1999 wiki NPC (7720 pages), the Items wiki (11,089 pages) and inserts the data into a normalized database. Here is the database design:

![](https://cdn.discordapp.com/attachments/617825237752479751/1183952717689933834/image.png?ex=658a34e4&is=6577bfe4&hm=92600486064b94d9dc480ac408c62af97a59d21a0416d4d718d40e1ebbba4e23&)

The database file is located in data/master.db (SQLite)

The database is already created. However, you could run main.py if for whatever reason, you wanted to run the program.

## Instructions:

- activate the venv: .venv/scripts/activate
- run python main.py

Thats it!

The program first creates the tables, then scrapes the URL's needed and saves them into a JSON file. Then, it iterates over the JSON file, and scrapes every URL and INSERTs the parsed pages into the database.
The tables 'item_master' and 'npc_master' must be created and filled first, due to other tables being 'dependent' on them (Foreign Keys).

I created the items scrape after the npc scrapes. The item scrape is superior, because I implemented async html fetches, which speeds up the scraping process a fair amount. I will eventually go back and refactor the NPC calls to be async as well.


