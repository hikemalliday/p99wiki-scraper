import sqlite3
import config

def alter_tables():
    conn = sqlite3.connect(config.database)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE UNIQUE INDEX idx_unique_zone_name ON zone_master(zone_name);
    ''')
    
    cursor.execute('''
        CREATE UNIQUE INDEX idx_unique_npc_zone ON npc_zone(zone_id, npc_id);
    ''')

    print('indexes added yo zone_master and npc_zone.')

def drop_zones_tables():
    conn = sqlite3.connect(config.database)
    cursor = conn.cursor()

    cursor.execute("""DROP TABLE zone_master""")
    cursor.execute("""DROP TABLE npc_zone""")

    conn.commit()
    conn.close()
    print('zone_master and npc_zone tables DROPPED')

def drop_special_tables():
    conn = sqlite3.connect(config.database)
    cursor = conn.cursor()

    cursor.execute("""DROP TABLE special_master""")
    cursor.execute("""DROP TABLE npc_special""")

    conn.commit()
    conn.close()
    print('specials tables DROPPED')

def drop_item_tables():
    conn = sqlite3.connect(config.database)
    cursor = conn.cursor()

    cursor.execute("""DROP TABLE item_master""")
    cursor.execute("""DROP TABLE npc_loot""")
    cursor.execute("""DROP TABLE npc_sold""")

    conn.commit()
    conn.close()
    print('items tables DROPPED')

def drop_faction_tables():
    conn = sqlite3.connect(config.database)
    cursor = conn.cursor()

    cursor.execute("""DROP TABLE faction_master""")
    cursor.execute("""DROP TABLE npc_faction""")

    conn.commit()
    conn.close()
    print('faction tables DROPPED')
