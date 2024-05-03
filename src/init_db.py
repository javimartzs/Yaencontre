import psycopg2
import os

def environment_vars():

    # Obtiene las variables de entorno
    username = 'postgres'
    password = 'gagll1i1'
    host = 'localhost'
    port = '5432'
    database = 'yaencontre'

    print(username, password, host, port, database)
    return username, password, host, port, database


def create_database_and_table():
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
            CREATE TABLE IF NOT EXISTS extraction (
                time VARCHAR(20),
                reference VARCHAR(50),
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
        print('Tabla de extraction creada existosamente')

        cursor.close()
        conn.close()

    except Exception as e:
        print('Error al crear la tabla:', e)



def drop_database_and_table():

    username, password, host, port, database = environment_vars()

    try:
        conn = psycopg2.connect(
            user = username,
            password = password, 
            host = host, 
            port = port
        )

        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(f"DROP DATABASE {database}")

        cursor.close()
        conn.close()
        print('Base de datos eliminada correctamente')

    except Exception as e:
        print(f'Error al eliminar la database: {e}')