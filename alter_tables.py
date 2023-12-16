import sqlite3
import config

# Used for the building / debugging process
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
