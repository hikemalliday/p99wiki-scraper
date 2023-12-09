import sqlite3
import config
import tables

def create_tables():
    conn = sqlite3.connect(config.database)
    c = conn.cursor()
    c.execute(tables.sql_npc_urls_table)
    c.execute(tables.sql_npc_data_table)
    c.execute(tables.sql_npc_loot_table)
    c.execute(tables.sql_npc_faction_table)
    c.execute(tables.sql_npc_opposing_faction_table)
    c.execute(tables.sql_npc_faction_hit_table)
    c.execute(tables.sql_item_data_table)
    c.execute(tables.sql_item_class_table)
    c.execute(tables.sql_item_race_table)
    c.execute(tables.sql_item_drop_table)
    c.execute(tables.sql_item_sold_table)
    conn.commit()
    conn.close()