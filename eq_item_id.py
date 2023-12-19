import mysql.connector
from mysql.connector import Error
import config
import sqlite3
import json

def connect_to_quarm_test():
    try:
        quarm_connect = mysql.connector.connect(
                host=config.host,
                port=config.port,
                user=config.user,
                password=config.password,
                database=config.quarm_db
            )
        quarm_connect.close()
        print('connected and closed successfully!')
    except Error as e:
        print('Error connecting to DB!' + str(e))
    

def connect_to_databases() -> tuple:
    try:
        quarm_connect = mysql.connector.connect(
            host=config.host,
            port=config.port,
            user=config.user,
            password=config.password,
            database=config.quarm_db
        )
        quarm_c = quarm_connect.cursor()
        master_connect = sqlite3.connect(config.database)
        master_c = master_connect.cursor()
    except:
        print('Error connecting to databases!')
        return ('Error', 'Error', 'Error', 'Error')

    return (master_connect, quarm_connect, quarm_c, master_c)

def insert_eq_item_ids():
    
    master_connect, quarm_connect, quarm_c, master_c = connect_to_databases()

    master_c.execute('''SELECT item_name FROM item_master''')
    item_names = master_c.fetchall()
    
    if item_names:
        # iterate over the 'item_names' tuple, and slice at the proper location
        with open('./data/latest_inserted_item_id.json', 'r') as latest_inserted_item:
            latest_inserted_item = json.load(latest_inserted_item)
            if latest_inserted_item:
                latest_inserted_item = latest_inserted_item[0]
                found_latest_item = False
                while found_latest_item == False:
                    for index, item_name in enumerate(item_names):
                        if item_name == latest_inserted_item:
                            item_names = item_names[index:]
                            found_latest_item = True
                            break
            else:
                print('Starting eq_item_id migration for the first time...')
            counter = 0
            for item_name in item_names:
                item_name = item_name[0]
                
                try:
                    
                    quarm_c.execute('''SELECT id FROM items WHERE name = %s''', (item_name,))
                    item_id = quarm_c.fetchall()
                    
                    if len(item_id) != 0:
                        master_c.execute('''SELECT eq_item_id FROM item_master WHERE item_name = ?''', (item_name,))
                        existing_eq_item_id = master_c.fetchone()[0]
                        if existing_eq_item_id == None:
                            print(item_id)
                            print(item_name)
                            item_id = item_id[0][0]
                            try:
                                master_c.execute('''UPDATE item_master SET eq_item_id = ? WHERE item_name = ?''', (item_id, item_name))
                                master_connect.commit()
                                counter += 1
                            except Exception as e:
                                print(e)
                        else:
                            print(f'Item {item_name} already has eq_item_id {existing_eq_item_id}, skipping update')
                              
                except Error as e:
                    print(e)
                    print(counter)
                    print(f'master item name: ' + str(item_name))
                    
            print('big test')
            print(counter)
            quarm_connect.close()
            master_connect.close()
                    
    else:
        print('item_names SELECT failed, aborting function...')
        return

insert_eq_item_ids()         

    





# This script takes the 'eq_item_id' from the 'Project Quarm' database, and inserts them into 'items_master'
# This was needed, because this special ID is commonly used in Everquest, and it is not on the Project1999 wiki

