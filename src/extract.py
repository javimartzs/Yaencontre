from selenium import webdriver
from time import sleep
import requests
import psycopg2


# Target cities
cities = [
    'madrid', 'coruna-a', 'barcelona', 'valencia', 'sevilla', 'malaga', 'murcia', 'palma-de-mallorca', 'palmas-de-gran-canaria-las', 
    'bilbao', 'cordoba', 'valladolid', 'vigo', 'gijon', 'hospitalet-de-llobregat-l', 'vitoria-gasteiz', 'elche-elx', 'granada', 
    'terrassa', 'badalona', 'cartagena', 'sabadell', 'oviedo', 'jerez-de-la-frontera', 'mostoles', 'pamplona-iruna', 'santa-cruz-de-tenerife', 
    'almeria', 'alcala-de-henares','fuenlabrada', 'san-sebastian-donostia', 'san-sebastian-de-los-reyes', 'leganes', 'getafe', 
    'burgos', 'albacete', 'castellon-de-la-plana-castello-de-la-plana', 'santander', 'alcorcon', 'san-cristobal-de-la-laguna', 
    'marbella', 'badajoz', 'logrono', 'salamanca', 'huelva', 'lleida', 'dos-hermanas', 'tarragona', 'torrejon-de-ardoz', 'parla', 
    'mataro', 'algeciras', 'leon', 'tres-cantos', 'guadalajara', 'ciudad-real', 'zaragoza', 'aranjuez', 'zamora', 'merida', 'alcoy-alcoi', 
    'motril', 'girona', 'alcobendas', 'cadiz', 'jaen', 'reus', 'ourense', 'telde', 'barakaldo', 'santiago-de-compostela', 'lugo', 
    'lorca', 'rivas-vaciamadrid', 'sant-cugat-del-valles', 'rozas-de-madrid-las', 'caceres', 'toledo', 'melilla', 'torrent', 'coslada', 
    'ceuta', 'pontevedra', 'arona', 'fuengirola', 'orihuela', 'rubi', 'valdemoro', 'manresa', 'getxo', 'palencia', 'gandia', 'aviles', 
    'ibiza', 'segovia', 'torrelavega', 'villareal', 'utrera', 'siero', 'elda', 'calviá', 'huesca', 'cuenca', 'pinto', 'linares', 
    'avila', 'granollers', 'irun', 'ponferrada', 'ferrol', 'arrecife', 'viladecans', 'castelldefels', 'sagunto', 'torremolinos', 
    'benidorm', 'paterna', 'majadahonda', 'benalmadena', 'estepona', 'torrevieja', 'velez-malaga', 'mijas', 'san-fernando', 
    'ejido-el', 'santa-coloma-de-gramanet', 'roquetas-de-mar', 'puerto-de-santa-maria-el', 'chiclana-de-la-frontera', 'molina-de-segura', 
    'sant-boi-de-llobregat', 'talavera-de-la-reina', 'alcala-de-guadaira', 'santa-lucia-de-tirajana', 'sanlucar-de-barrameda', 
    'prat-de-llobregat-el', 'colmenar-viejo', 'arganda-del-rey', 'boadilla-del-monte', 'collado-villalba', 'mollet-del-valles', 
    'rincon-de-la-victoria', 'granadilla-de-abona', 'san-bartolome-de-tirajana', 'linea-de-la-concepcion-la', 'san-vicente-del-raspeig', 
    'sardanola-del-valles', 'alicante-alacant'
]


# Init connection function
def init_connection():
    conn = psycopg2.connect(
        user="postgres",
        password="gagll1i1",
        host="localhost",
        port="5432",
        database="yaencontre"
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

    operations = ['RENT', 'BUY']

    for city in cities:
        for operation in operations:
            url = f'https://www.yaencontre.com/alquiler/pisos/{city}'
            s = get_cookies(url)

            api = f'https://api.yaencontre.com/v3/search?family=FLAT&lang=es&location={city}&operation={operation}&pageSize=42'
            response = s.get(api)
            data = response.json()
            pages = data['result']['numPages']
            print(f'La ciudad de {city} en {operation} tiene {pages} páginas')


            for i in range(1, pages+1):
                api = f'https://api.yaencontre.com/v3/search?family=FLAT&lang=es&location={city}&operation={operation}&pageSize=42&pageNumber={i}'
                response = s.get(api)
                data = response.json()
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
                            INSERT INTO information (id, reference, title, description, operation, family, owner_type, owner_id, owner_name, price, size, rooms, bathrooms, new, address, latitude, longitude, city)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ''', 
                        (id_, reference, title, description, operation, family, owner_type, owner_id, owner_name, price, size, rooms, bathrooms, new, address, latitude, longitude, city))
                
                print(f'Pagina {i} de {pages} añadida')
            print(f"Datos de {city} {operation} insertados exitosamente en la base de datos.")


# Run functions 
def fetch_and_insert_data():
    conn, cursor = init_connection()
    fetch_data_for_city(cursor, cities)
    close_connection(conn, cursor)
    print('Descarga terminada')