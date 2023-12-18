import npc_master
import npc_faction
import npc_item
import npc_special
import npc_zone
import item_master
import create_tables

if __name__ == "__main__":
    create_tables.create_tables()
    item_master.item_url_scrape()
    item_master.item_master_scrape()
    npc_master.npc_url_scrape()
    npc_master.npc_master_scrape()
    npc_faction.npc_faction_scrape()
    npc_item.npc_items_scrape()
    npc_special.npc_special_scrape()
    npc_zone.npc_zone_scrape()

