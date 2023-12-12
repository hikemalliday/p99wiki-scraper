import sqlite3
import config

def create_tables():
    try:
        conn = sqlite3.connect(config.database)
        cursor = conn.cursor()
    
        cursor.execute('''
        CREATE TABLE npc_master (
            npc_id INTEGER PRIMARY KEY AUTOINCREMENT,
            npc_name TEXT,
            npc_description TEXT,
            npc_race TEXT,
            npc_class,
            npc_min_level INTEGER,
            npc_max_level INTEGER,
            npc_respawn_time INTEGER,
            npc_AC INTEGER,
            npc_HP INTEGER,
            npc_min_damage_per_hit INTEGER,
            npc_max_damage_per_hit INTEGER,
            npc_attacks_per_round INTEGER
        );
        ''')

        cursor.execute('''
        CREATE TABLE item_master (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT UNIQUE
        );
        ''')

        cursor.execute('''
        CREATE TABLE faction_master (
            faction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            faction_name TEXT UNIQUE
        );
        ''')
        cursor.execute('''
        CREATE TABLE special_master (
            special_id INTEGER PRIMARY KEY AUTOINCREMENT,
            special_name TEXT UNIQUE
        );
        ''')

        cursor.execute('''
        CREATE TABLE zone_master (
            zone_id INTEGER PRIMARY KEY AUTOINCREMENT,
            zone_name TEXT UNIQUE
        );
        ''')

        cursor.execute('''
        CREATE TABLE npc_zone (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            zone_id INTEGER REFERENCES zone_master(zone_id),
            npc_id INTEGER REFERENCES npc_master(npc_id)
        );
        ''')
        cursor.execute('''
        CREATE TABLE npc_faction (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            npc_id INTEGER REFERENCES npc_master(npc_id),
            faction_id INTEGER REFERENCES faction_master(faction_id),
            hit INTEGER
        );
        ''')
        cursor.execute('''
        CREATE TABLE npc_special (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            special_id INTEGER REFERENCES special_master(special_id),
            npc_id INTEGER REFERENCES npc_master(npc_id)
        );
        ''')

        cursor.execute('''
        CREATE TABLE npc_loot (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            npc_id INTEGER REFERENCES npc_master(npc_id),
            item_id INTEGER REFERENCES item_master(item_id)
        );
        ''')

        cursor.execute('''
        CREATE TABLE npc_sold (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            npc_id INTEGER REFERENCES npc_master(npc_id),
            item_id INTEGER REFERENCES item_master(item_id)
        );
        ''')
        conn.commit()
        conn.close()
        print("Tables created.")
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")
        return f"Error creating tables: {e}"

