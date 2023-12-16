# p99wiki-scraper

###### A python based web scraping tool made to create a normalized database of https://wiki.project1999.com/Category:NPCs and https://wiki.project1999.com/Category:Items

This program scrapes the Project 1999 NPC wiki (7720 pages), the Items wiki (11,089 pages) and inserts the data into a normalized database. Here is the database design:

![](https://cdn.discordapp.com/attachments/617825237752479751/1185697501253218334/image.png?ex=65908dd9&is=657e18d9&hm=2c5030a01cf1b599a201f6e9ee52c79b8725b29ebf6f8f54b29ee3e3c01df97e&)

The database file is located in data/master.db (SQLite)

The database is already created. However, you could run main.py if for whatever reason, you wanted to run the program.

## Instructions:

- activate the venv: .venv/scripts/activate
- run python main.py

Thats it!

The program first creates the tables, then scrapes the URL's needed and saves them into a JSON file. Then, it iterates over the JSON file, and scrapes every URL and INSERTs the parsed pages into the database.
The 'root' table ('npc_master') is scraped first. The order of the other functions after these first few do no matter.
