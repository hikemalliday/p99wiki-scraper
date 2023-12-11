import sqlite3
import config

queries = {
    'One': ["""SELECT * FROM item_master WHERE item_name LIKE ?""", ('%Abashi%',)],
    'Two': [""'''
                SELECT item_master.item_name
                FROM npc_master
                JOIN npc_loot ON npc_master.npc_id = npc_loot.npc_id
                JOIN item_master ON npc_loot.item_id = item_master.item_id
                WHERE npc_master.npc_name = ?
        ''', 
              ('King Tormax',)],






    'Four': ['''
        SELECT faction_master.faction_name, npc_faction.hit, npc_master.npc_name
        FROM npc_master
        JOIN npc_faction ON npc_master.npc_id = npc_faction.npc_id
        JOIN faction_master ON npc_faction.faction_id = faction_master.faction_id
        WHERE npc_master.npc_name = ?
        ''', ('King Tormax',)],
    'Five': ["""SELECT * FROM item_master WHERE item_name LIKE ?""", ('%Abashi%',)],
    'Six': ["""SELECT * FROM item_master WHERE item_name LIKE ?""", ('%Abashi%',)],
    'Seven': ["""SELECT * FROM item_master WHERE item_name LIKE ?""", ('%Abashi%',)],
    'Eight': ["""SELECT * FROM item_master WHERE item_name LIKE ?""", ('%Abashi%',)],
    'Nine': ["""SELECT * FROM item_master WHERE item_name LIKE ?""", ('%Abashi%',)],
    'Ten': ["""SELECT * FROM item_master WHERE item_name LIKE ?""", ('%Abashi%',)],
}

def sql_query(query_string: str, parameters: tuple) -> list:
    conn = sqlite3.connect(config.database)
    c = conn.cursor()
    c.execute(query_string, parameters)
    results = c.fetchall()
    return results

print(sql_query(queries['Four'][0], queries['Four'][1]))