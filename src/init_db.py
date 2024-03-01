import psycopg2
from dotenv import load_dotenv
import os


def environment_vars():
    load_dotenv()
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    database = os.getenv('DATABASE')
    
    return username, password, host, port, database, 



def create_database_and_tables():

    # Import environments variables
    username, password, host, port, database = environment_vars()

    # Create Postgres Database
    try:
        conn = psycopg2.connect(
            user = username, 
            password = password,
            host = host, 
            port = port
        )
        conn.autocommit = True
        cursor = conn.cursor()

        db_query = f'CREATE DATABASE {database};'
        cursor.execute(db_query)

        cursor.close()
        conn.close()
        print('Database creada existosamente')

    except Exception as e:
        print('Error al crear la base de datos:', e)
    

    # Create two tables in Postgres Database
    try:
        conn = psycopg2.connect(
            user = username, 
            password = password,
            host = host, 
            port = port,
            database = database
        )

        conn.autocommit = True
        cursor = conn.cursor()

        table_query = '''
            CREATE TABLE extraction (
                id VARCHAR(100), 
                reference VARCHAR(100),
                title TEXT,
                description TEXT,
                operation VARCHAR(100),
                family VARCHAR(100),
                owner_type VARCHAR(100),
                owner_id VARCHAR(100),
                owner_name TEXT, 
                price numeric,
                size numeric, 
                rooms numeric, 
                bathrooms numeric, 
                new VARCHAR(10), 
                address TEXT, 
                latitude numeric, 
                longitude numeric,
                location VARCHAR(100)
            )
        '''
        cursor.execute(table_query)
        print('Tabla de informacion creada existosamente')

        cursor.close()
        conn.close()

    except Exception as e:
        print('Error al crear la tabla:', e)
