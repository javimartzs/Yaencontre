from selenium import webdriver
import requests
import psycopg2

from init_db import create_database

ciudades = [
    "santa cruz de tenerife","pamplona","almería","alcalá de henares","fuenlabrada","san sebastián","leganés","getafe",
    "burgos","albacete","castellón de la plana","santander","alcorcón","san cristóbal de la laguna","marbella","badajoz",
    "logroño","salamanca","huelva","lérida","dos hermanas","tarragona","torrejón de ardoz","parla","mataró","algeciras","león",
    "santa coloma de gramenet","alcobendas","cádiz","jaén","reus","o-rense","roquetas de mar","gerona","telde","baracaldo",
    "santiago de compostela","lugo","lorca","rivas-vaciamadrid","sant cugat del vallès","las rozas","cáceres","san fernando",
    "san sebastián de los reyes","mijas","puerto de santa maría","el ejido","chiclana de la frontera","melilla","torrent","toledo",
    "vélez-málaga","torrevieja","sant boi de llobregat","talavera de la reina","fuengirola","ceuta","arona","pontevedra","orihuela",
    "coslada","valdemoro","rubí","manresa","getxo","palencia","alcalá de guadaíra","gandia","avilés","molina de segura",
    "santa lucía de tirajana","estepona","benalmádena","majadahonda","paterna","benidorm","sanlúcar de barrameda","torremolinos",
    "sagunto","castelldefels","viladecans","el prat de llobregat","collado villalba","ferrol","arrecife","línea de la concepción",
    "ponferrada","irún","boadilla del monte","granollers","aranjuez","zamora","mérida","san vicente del raspeig","alcoy","motril",
    "ávila","arganda del rey","sardañola del vallès","linares","pinto","cuenca","colmenar viejo","huesca","san bartolomé de tirajana",
    "calviá","granadilla de abona","elda","siero","utrera","villarreal","mollet del vallès","torrelavega","segovia","ibiza",
    "rincón de la victoria","tres cantos","guadalajara","zaragoza","ciudad real"
]

cities = [
    'madrid', 'coruna-a', 'barcelona', 'valencia', 'sevilla', 'malaga', 'murcia', 'palma-de-mallorca', 'palmas-de-gran-canaria-las', 'bilbao', 
    'alicante', 'cordoba', 'valladolid', 'vigo', 'gijon', 'hospitalet-de-llobregat-l', 'vitoria-gasteiz', 'elche', 'granada', 'terrasa', 'badalona', 
    'cartagena', 'sabadell', 'oviedo', 'jerez-de-la-frontera', 'mostoles', 'pamplona', 'santa-cruz-de-tenerife', 'almeria', 'alcala-de-henares',
    'fuenlabrada', 'san-sebastian', 'leganes', 'getafe', 'burgos', 'albacete', 'castellon-de-la-plana-castello-de-la-plana', 'santander', 'alcorcon', 
    ]

def fetch_and_insert_data():
    # Iniciamos la conexion con la base de datos
    conn = psycopg2.connect(
        user="postgres",
        password="gagll1i1",
        host="localhost",
        port="5432",
        database="yaencontre"
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Proceso para guardar las cookies 
    url = 'https://www.yaencontre.com/alquiler/pisos/madrid'

    driver = webdriver.Chrome()
    driver.get(url)

    cookies = driver.get_cookies()
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])

    driver.close()

    for city in cities:

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


            # Extraer datos de la api
            for item in items:
                build = item['realEstate']
                id_ = build['id']
                reference = build['reference']
                title = build['title']

                if 'description' in build:
                    description = build['description'].replace('\n', ' ')
                else:
                    description = None
                    
                operation = build['operation']
                family = build['family']
                owner_type = build['owner']['type']

                if 'commercialId' in build['owner']:
                    owner_id = build['owner']['commercialId']
                else:
                    owner_id = None

                if 'name' in build['owner']:
                    owner_name = build['owner']['name']
                else:
                    owner_name = None
                
                price = build['price']
                size = build['area']

                if 'rooms' in build:
                    rooms = build['rooms']
                else:
                    rooms = None

                if 'bathrooms' in build:
                    bathrooms = build['bathrooms']
                else:
                    bathrooms = None

                new = build['isNewConstruction']
                latitude = build['address']['geoLocation']['lat']
                longitude = build['address']['geoLocation']['lon']


                ciudad = city

                cursor.execute('''
                    INSERT INTO information (id, reference, title, description, operation, family, owner_type, owner_id, owner_name, price, size, rooms, bathrooms, new, latitude, longitude, city)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', 
                (id_, reference, title, description, operation, family, owner_type, owner_id, owner_name, price, size, rooms, bathrooms, new, latitude, longitude, ciudad))


            print(f'Pagina {i} de {pages} añadida')
        print(f"Datos de {city} insertados exitosamente en la base de datos.")

    cursor.close()
    conn.close()
    print('Descargar terminada')





if __name__ == "__main__":
    create_database()
    fetch_and_insert_data()