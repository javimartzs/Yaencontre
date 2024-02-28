from selenium import webdriver
from time import sleep
import requests
import psycopg2

ciudades = [
    "santa coloma de gramenet",
    "roquetas de mar",
    "san fernando",
    "mijas",
    "puerto de santa maría",
    "el ejido",
    "chiclana de la frontera",
    "vélez-málaga",
    "torrevieja",
    "sant boi de llobregat",
    "talavera de la reina",
    "alcalá de guadaíra",
    "molina de segura",
    "santa lucía de tirajana",
    "estepona",
    "benalmádena","majadahonda","paterna","benidorm","sanlúcar de barrameda","torremolinos",
    "sagunto",
    "castelldefels","viladecans","el prat de llobregat","collado villalba","ferrol","arrecife","línea de la concepción",
    "ponferrada",
    "irún","boadilla del monte","granollers","san vicente del raspeig"
    "ávila",
    "arganda del rey","sardañola del vallès","linares","pinto","cuenca","colmenar viejo","huesca","san bartolomé de tirajana",
    "calviá",
    "granadilla de abona",
    "elda",
    "siero",
    "utrera",
    "villarreal",
    "mollet del vallès",
    "torrelavega",
    "segovia",
    "ibiza",
    "rincón de la victoria"
]

cities = [
    'madrid', 'coruna-a', 'barcelona', 'valencia', 'sevilla', 'malaga', 'murcia', 'palma-de-mallorca', 'palmas-de-gran-canaria-las', 
    'bilbao', 'cordoba', 'valladolid', 'vigo', 'gijon', 'hospitalet-de-llobregat-l', 'vitoria-gasteiz', 'elche-elx', 'granada', 
    'terrassa', 'badalona', 'cartagena', 'sabadell', 'oviedo', 'jerez-de-la-frontera', 'mostoles', 'pamplona-iruna', 'santa-cruz-de-tenerife', 
    'almeria', 'alcala-de-henares','fuenlabrada', 'san-sebastian-donostia', 'san-sebastian-de-los-reyes', 'leganes', 'getafe', 
    'burgos', 'albacete', 'castellon-de-la-plana-castello-de-la-plana', 'santander', 'alcorcon', 'san-cristobal-de-la-laguna', 
    'marbella', 'badajoz', 'logrono', 'salamanca', 'huelva', 'lleida', 'dos-hermanas', 'tarragona', 'torrejon-de-ardoz', 'parla', 
    'mataro', 'algeciras', 'leon', 'tres-cantos', 'guadalajara', 'ciudad-real', 'zaragoza', 'aranjuez', 'zamora', 'merida', 'alcoy', 
    'motril', 'girona', 'alcobendas', 'cadiz', 'jaen', 'reus', 'ourense', 'telde', 'barakaldo', 'santiago-de-compostela', 'lugo', 
    'lorca', 'rivas-vaciamadrid', 'sant-cugat-del-valles', 'rozas-de-madrid-las', 'caceres', 'toledo', 'melilla', 'torrent', 'coslada', 
    'ceuta', 'pontevedra', 'arona', 'fuengirola', 'orihuela', 'rubi', 'valdemoro', 'manresa', 'getxo', 'palencia', 'gandia', 'aviles', 
    'ibiza', 'segovia', 'torrelavega', 'villareal', 'utrera', 'siero', 'elda', 'calviá', ''
    ]



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

def close_connection(conn, cursor):
    cursor.close()
    conn.close()

def get_cookies(url):
    driver = webdriver.Chrome()
    driver.get(url)
    cookies = driver.get_cookies()
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    driver.close()
    return s

def fetch_data_for_city(cursor, cities):
    for city in cities:

        url = f'https://www.yaencontre.com/alquiler/pisos/{city}'
        s = get_cookies(url)

        api = f'https://api.yaencontre.com/v3/search?family=FLAT&lang=es&location={city}&operation=RENT&pageSize=42'
        response = s.get(api)
        data = response.json()
        pages = data['result']['numPages']
        print(pages)

        for i in range(1, pages+1):
            api = f'https://api.yaencontre.com/v3/search?family=FLAT&lang=es&location={city}&operation=RENT&pageSize=42&pageNumber={i}'
            response = s.get(api)
            data = response.json()
            items = data['result']['items']
            for item in items:
                build = item['realEstate']
                id_ = build['id']
                reference = build['reference']
                title = build['title']
                description = build.get('description', None)
                operation = build['operation']
                family = build['family']
                owner_type = build['owner']['type']
                owner_id = build['owner'].get('commercialId', None)
                owner_name = build['owner'].get('name', None)
                price = build['price']
                size = build['area']
                rooms = build.get('rooms', None)
                bathrooms = build.get('bathrooms', None)
                new = build['isNewConstruction']
                latitude = build['address']['geoLocation']['lat']
                longitude = build['address']['geoLocation']['lon']
                
                cursor.execute('''
                    INSERT INTO information (id, reference, title, description, operation, family, owner_type, owner_id, owner_name, price, size, rooms, bathrooms, new, latitude, longitude, city)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', 
                (id_, reference, title, description, operation, family, owner_type, owner_id, owner_name, price, size, rooms, bathrooms, new, latitude, longitude, city))
            
            print(f'Pagina {i} de {pages} añadida')
        
        print(f"Datos de {city} insertados exitosamente en la base de datos.")


def fetch_and_insert_data():
    conn, cursor = init_connection()
    fetch_data_for_city(cursor, cities)
    close_connection(conn, cursor)
    print('Descarga terminada')