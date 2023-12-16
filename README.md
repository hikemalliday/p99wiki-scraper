# p99wiki-scraper

###### A python based web scraping tool made to create a normalized database of https://wiki.project1999.com/Category:NPCs and https://wiki.project1999.com/Category:Items

This program scrapes the Project 1999 wiki NPC (7720 pages), the Items wiki (11,089 pages) and inserts the data into a normalized database. Here is the database design:

![](https://cdn.discordapp.com/attachments/617825237752479751/1185615375128330362/image.png?ex=6590415d&is=657dcc5d&hm=f1f03f6d835386dc87bba86c4c23b50051e192e8427ebdfd74420a4b5bbfdacd&)

The database file is located in data/master.db (SQLite)

The database is already created. However, you could run main.py if for whatever reason, you wanted to run the program.

## Instructions:

- activate the venv: .venv/scripts/activate
- run python main.py

Thats it!

The program first creates the tables, then scrapes the URL's needed and saves them into a JSON file. Then, it iterates over the JSON file, and scrapes every URL and INSERTs the parsed pages into the database.
The 'root' table ('npc_master') is scraped first. The order of the other functions after these first few do no matter.
