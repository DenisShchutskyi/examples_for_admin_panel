import psycopg2
from config import str_connect_to_db


def create_connection():
    """
    метод создания подключения к БД
    :return: или подключение или None
    """
    conn = None
    try:
        conn = psycopg2.connect(str_connect_to_db)
    except:
        print ("I am unable to connect to the database")
    return conn