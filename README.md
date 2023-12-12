# p99wiki-scraper
###### A python based web scraping tool I made to create a normalized database of https://wiki.project1999.com/Category:NPCs

I scraped the Project 1999 wiki NPC (7720 pages), and inserted the data into a normalized database. Here is the database design:

![](https://cdn.discordapp.com/attachments/617825237752479751/1183952717689933834/image.png?ex=658a34e4&is=6577bfe4&hm=92600486064b94d9dc480ac408c62af97a59d21a0416d4d718d40e1ebbba4e23&)

The database file is located in data/master.db (SQLite)

The database is already created. However, you could run main.py if for whatever reason, you wanted to run the program.

## Instructions:

- activate the venv: .venv/scripts/activate
- run python main.py

Thats it!

The program first creates the tables, then scrapes the URL's needed and saves them into a JSON file. Then, it iterates over the JSON file, and scrapes every URL and INSERTs into the database.
The 'root' table is scraped first 'npc_master'. The order of the other functions after these first few do no matter.


I will eventually use the database for future projects. Soon I will also do a complete scrape / db creation of the Items pages as well.
