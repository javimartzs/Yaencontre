from init_db import create_database_and_tables
from extract import fetch_and_insert_data
import time

if __name__ == "__main__":
    start_time = time.time()  # Registro del tiempo de inicio
    create_database_and_tables()
    fetch_and_insert_data()
    end_time = time.time()  # Registro del tiempo de finalización
    print(f'Tiempo transcurrido: {(end_time - start_time)/60} minutos')