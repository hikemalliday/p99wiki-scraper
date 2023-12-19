import npc_master
import npc_faction
import npc_item
import npc_special
import npc_zone
import item_master
import create_tables
import asyncio

if __name__ == "__main__":
    create_tables.create_tables()
    item_master.item_url_scrape()
    npc_master.npc_url_scrape()
    asyncio.run(item_master.item_master_scrape())
    asyncio.run(npc_master.npc_master_scrape())
    asyncio.run(npc_faction.npc_faction_scrape())
    asyncio.run(npc_item.npc_items_scrape())
    asyncio.run(npc_special.npc_special_scrape())
    asyncio.run(npc_zone.npc_zone_scrape())

