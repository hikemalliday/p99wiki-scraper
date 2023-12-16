import sqlite3
import config

def create_tables():
    try:
        conn = sqlite3.connect(config.database)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE npc_master (
            npc_id INTEGER PRIMARY KEY AUTOINCREMENT,
            npc_name TEXT UNIQUE,
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
        cursor.execute('''CREATE INDEX idx_npc_name ON npc_master(npc_name);''')

        cursor.execute('''
        CREATE TABLE item_master (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT UNIQUE,
            item_magic BOOLEAN,
            item_lore BOOLEAN,
            item_no_drop BOOLEAN,
            item_no_rent BOOLEAN,
            item_expendable BOOLEAN,
            item_quest BOOLEAN,
            item_dmg INTEGER,
            item_delay INTEGER,
            item_ac INTEGER,
            item_effect TEXT,
            item_hp INTEGER,
            item_mp INTEGER,
            item_str INTEGER,
            item_sta INTEGER,
            item_dex INTEGER,
            item_agi INTEGER,
            item_wis INTEGER,
            item_int INTEGER,
            item_cha INTEGER,
            item_sv_fire INTEGER,
            item_sv_disease INTEGER,
            item_sv_cold INTEGER,
            item_sv_magic INTEGER,
            item_sv_poison INTEGER,
            item_wt FLOAT,
            item_size TEXT,
            item_image TEXT
        );
        
        ''')

        cursor.execute('''CREATE INDEX idx_item_name ON item_master(item_name);''')

        cursor.execute('''
        CREATE TABLE item_class (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER REFERENCES item_master(item_id),
            item_enc BOOLEAN,
            item_mag BOOLEAN,
            item_nec BOOLEAN,
            item_wiz BOOLEAN,
            item_clr BOOLEAN,
            item_dru BOOLEAN,
            item_shm BOOLEAN,
            item_brd BOOLEAN,
            item_mnk BOOLEAN,
            item_rng BOOLEAN,
            item_rog BOOLEAN,
            item_pal BOOLEAN,
            item_shd BOOLEAN,
            item_war BOOLEAN
        );
''')
        
        cursor.execute('''
        CREATE TABLE item_race (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER REFERENCES item_master(item_id),
            item_bar BOOLEAN,
            item_def BOOLEAN,
            item_dwf BOOLEAN,
            item_eru BOOLEAN,
            item_gnm BOOLEAN,
            item_hef BOOLEAN,
            item_hfl BOOLEAN,
            item_hie BOOLEAN,
            item_hum BOOLEAN,
            item_iks BOOLEAN,
            item_ogr BOOLEAN,
            item_trl BOOLEAN,
            item_elf BOOLEAN
        );
''')
        
        cursor.execute('''
        CREATE TABLE item_slot (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER REFERENCES item_master(item_id),
            item_primary BOOLEAN,
            item_secondary BOOLEAN,
            item_range BOOLEAN,
            item_arms BOOLEAN,
            item_back BOOLEAN,
            item_chest BOOLEAN,
            item_ear BOOLEAN,
            item_face BOOLEAN,
            item_feet BOOLEAN,
            item_fingers BOOLEAN,
            item_hands BOOLEAN,
            item_head BOOLEAN,
            item_legs BOOLEAN,
            item_neck BOOLEAN,
            item_shoulders BOOLEAN,
            item_waist BOOLEAN,
            item_wrist BOOLEAN,
            item_ammo BOOLEAN
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

create_tables()