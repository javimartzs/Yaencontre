from init_db import create_database_and_table, drop_database_and_table
from extract import fetch_and_insert_data
import time

if __name__ == "__main__":
    start_time = time.time() 
    create_database_and_table()
    fetch_and_insert_data()
    drop_database_and_table()
    end_time = time.time()  
    print(f'Tiempo transcurrido: {(end_time - start_time)/60} minutos')