from init_db import create_database_and_table, drop_database_and_table
from extract import fetch_and_insert_data
import time
import psycopg2

if __name__ == "__main__":

    start_time = time.time()        # Iniciar temporizador
    create_database_and_table()     # Crear base de datos y tabla
    fetch_and_insert_data()         # Extraer datos y almacenar en parquet
    drop_database_and_table()       # Eliminar base de datos y tabla
    end_time = time.time()          # Finalizar temporizador

    print(f'Tiempo transcurrido: {(end_time - start_time)/60} minutos')