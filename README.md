# p99wiki-scraper

###### A python based web scraping tool made to create a normalized database of https://wiki.project1999.com/Category:NPCs and https://wiki.project1999.com/Category:Items

This program scrapes the Project 1999 wiki NPC (7720 pages), the Items wiki (11,089 pages) and inserts the data into a normalized database. Here is the database design:

![](https://cdn.discordapp.com/attachments/617825237752479751/1185697063971860600/image.png?ex=65908d71&is=657e1871&hm=c8f8a95d5d606c963afc01ed93703f98aa1960b0d6e5aafc933c6808548b32b1&)

The database file is located in data/master.db (SQLite)

The database is already created. However, you could run main.py if for whatever reason, you wanted to run the program.

## Instructions:

- activate the venv: .venv/scripts/activate
- run python main.py

Thats it!

The program first creates the tables, then scrapes the URL's needed and saves them into a JSON file. Then, it iterates over the JSON file, and scrapes every URL and INSERTs the parsed pages into the database.
The 'root' table ('npc_master') is scraped first. The order of the other functions after these first few do no matter.
