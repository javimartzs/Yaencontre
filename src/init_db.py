import psycopg2

def create_database():

    try:
        conn = psycopg2.connect(
            user = 'postgres', 
            password = 'gagll1i1',
            host = 'localhost', 
            port = '5432'
        )
        conn.autocommit = True
        cursor = conn.cursor()

        db_query = 'CREATE DATABASE yaencontre;'
        cursor.execute(db_query)

        cursor.close()
        conn.close()
        print('Database creada existosamente')

    except Exception as e:
        print('Error al crear la base de datos:', e)


    try:
        conn = psycopg2.connect(
            user = 'postgres',
            password = 'gagll1i1', 
            host = 'localhost', 
            port = '5432', 
            database = 'yaencontre'
        )
        conn.autocommit = True
        cursor = conn.cursor()

        table_query = '''
            CREATE TABLE information (
                
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
                city VARCHAR(50)
            )
        '''
        cursor.execute(table_query)
        print('Tabla creada existosamente')

        cursor.close()
        conn.close()

    except Exception as e:
        print('Error al crear la tabla:', e)
