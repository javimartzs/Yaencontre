from selenium import webdriver
from init_db import environment_vars
import requests
import psycopg2


# Target cities
cities = [
    'madrid', 'barcelona', 'valencia', 'sevilla', 'malaga', 'murcia', 'coruna-a', 'palma-de-mallorca', 'palmas-de-gran-canaria-las', 
    'bilbao', 'cordoba', 'valladolid', 'vigo', 'gijon', 'hospitalet-de-llobregat-l', 'vitoria-gasteiz', 'elche-elx', 'granada', 
    'terrassa','badalona', 'cartagena', 'sabadell', 'oviedo', 'jerez-de-la-frontera', 'mostoles', 'pamplona-iruna', 'santa-cruz-de-tenerife', 
    'almeria', 'alcala-de-henares','fuenlabrada', 'san-sebastian-donostia', 'san-sebastian-de-los-reyes', 'leganes', 'getafe', 
    'burgos', 'albacete', 'castellon-de-la-plana-castello-de-la-plana', 'santander', 'alcorcon', 'san-cristobal-de-la-laguna', 
    'marbella', 'badajoz', 'logrono', 'salamanca', 'huelva', 'lleida', 'dos-hermanas', 'tarragona', 'torrejon-de-ardoz', 'parla', 
    'mataro', 'algeciras', 'leon', 'tres-cantos', 'guadalajara', 'ciudad-real', 'zaragoza', 'aranjuez', 'zamora', 'merida', 'alcoy-alcoi', 
    'motril', 'girona', 'alcobendas', 'cadiz', 'jaen', 'reus', 'ourense', 'telde', 'barakaldo', 'santiago-de-compostela', 'lugo', 
    'lorca', 'rivas-vaciamadrid', 'sant-cugat-del-valles', 'rozas-de-madrid-las', 'caceres', 'toledo', 'melilla', 'torrent', 'coslada', 
    'ceuta', 'pontevedra', 'arona', 'fuengirola', 'orihuela', 'rubi', 'valdemoro', 'manresa', 'getxo', 'palencia', 'gandia', 'aviles', 
    'ibiza-eivissa', 'segovia', 'torrelavega', 'villarreal-vila-real', 'utrera', 'siero', 'elda', 'calvia', 'huesca', 'cuenca', 'pinto', 'linares', 
    'avila', 'granollers', 'irun', 'ponferrada', 'ferrol', 'arrecife', 'viladecans', 'castelldefels', 'sagunto-sagunt', 'torremolinos', 
    'benidorm', 'paterna', 'majadahonda', 'benalmadena', 'estepona', 'torrevieja', 'velez-malaga', 'mijas', 'san-fernando', 
    'ejido-el', 'santa-coloma-de-gramanet', 'roquetas-de-mar', 'puerto-de-santa-maria-el', 'chiclana-de-la-frontera', 'molina-de-segura', 
    'sant-boi-de-llobregat', 'talavera-de-la-reina', 'alcala-de-guadaira', 'santa-lucia-de-tirajana', 'sanlucar-de-barrameda', 
    'prat-de-llobregat-el', 'colmenar-viejo', 'arganda-del-rey', 'boadilla-del-monte', 'collado-villalba', 'mollet-del-valles', 
    'rincon-de-la-victoria', 'granadilla-de-abona', 'san-bartolome-de-tirajana', 'linea-de-la-concepcion-la', 'alicante-alacant', 
    'san-vicente-del-raspeig-sant-vicent-del-raspeig', 'cerdanyola-del-valles'
]


# Init connection function
def init_connection():

    username, password, host, port, database = environment_vars()

    conn = psycopg2.connect(
        user = username, 
        password = password,
        host = host, 
        port = port,
        database = database
    )
    conn.autocommit = True
    cursor = conn.cursor()
    return conn, cursor

# Close connection function
def close_connection(conn, cursor):
    cursor.close()
    conn.close()


# Get cookies function
def get_cookies(url):
    driver = webdriver.Chrome()
    driver.get(url)
    cookies = driver.get_cookies()
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    driver.close()
    return s


# Extract and load data function
def fetch_data_for_city(cursor, cities):

    for city in cities:
        # Obtencion de las cookies 
        url = f'https://www.yaencontre.com/alquiler/pisos/{city}'
        s = get_cookies(url)

        # Obtencion de los municipios dentro de cada provincia
        api = f'https://api.yaencontre.com/v3/search?family=FLAT&lang=es&location={city}&operation=RENT&pageSize=42'
        response = s.get(api)
        data = response.json()

        # Obtencion del numero de paginas por provincia
        pages = data['result']['numPages']
        print(f'La ciudad de {city} tiene {pages} páginas')

        # Obtencion de la informacion de precios pagina a pagina por provincia
        for i in range(1, pages+1):
            api = f'https://api.yaencontre.com/v3/search?family=FLAT&lang=es&location={city}&operation=RENT&pageSize=42&pageNumber={i}'
            response = s.get(api)
            data = response.json()

            location = data['result']['location']
            items = data['result']['items']

            for item in items:
                build = item['realEstate']
                id_ = build.get('id', None)
                reference = build.get('reference', None)
                title = build.get('title', None)
                description = build.get('description', None)
                operation = build.get('operation')
                family = build.get('family')
                owner_type = build['owner'].get('type', None)
                owner_id = build['owner'].get('commercialId', None)
                owner_name = build['owner'].get('name', None)
                price = build.get('price', None)
                size = build.get('area', None)
                rooms = build.get('rooms', None)
                bathrooms = build.get('bathrooms', None)
                new = build.get('isNewConstruction', None)
                address = build['address'].get('qualifiedName', None)
                latitude = build['address']['geoLocation']['lat']
                longitude = build['address']['geoLocation']['lon']

                cursor.execute(
                    '''
                        INSERT INTO extraction (
                            id, reference, title, description, operation, family, owner_type, owner_id, owner_name, 
                            price, size, rooms, bathrooms, new, address, latitude, longitude, location
                            )
                        VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                            )
                    ''', (
                        id_, reference, title, description, operation, family, owner_type, owner_id, owner_name, 
                        price, size, rooms, bathrooms, new, address, latitude, longitude, location
                        )
                )
            
            print(f'Pagina {i} de {pages} añadida')
        print(f"Datos de {city} insertados exitosamente en la base de datos.")


# Run functions 
def fetch_and_insert_data():
    conn, cursor = init_connection()
    fetch_data_for_city(cursor, cities)
    close_connection(conn, cursor)
    print('Descarga terminada')