import telebot
from dotenv import load_dotenv
import os
from os.path import join, dirname
import mysql.connector


def get_token(key):
    """ Возвращает ключи """
    token_path = join(dirname(__file__), '.env')
    load_dotenv(token_path)
    return os.environ.get(key)


token_db = get_token("DB_CONNECT")
print(token_db)
db = mysql.connector.connect(token_db)
