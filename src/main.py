from init_db import create_database
from extract import fetch_and_insert_data


if __name__ == "__main__":
    create_database()
    fetch_and_insert_data()