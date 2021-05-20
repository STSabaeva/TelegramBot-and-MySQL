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


bot = telebot.TeleBot(get_token("TELEGRAM_BOT_TOKEN"))
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='tatiana',
    port='3306',
    database='TelegramBot'
)

db_cursor = db.cursor()

""" Создание БД и таблицы"""

# db_cursor.execute("CREATE DATABASE TelegramBot")
# db_cursor.execute("CREATE TABLE users(id INT AUTO_INCREMENT PRIMARY "
#                   "KEY, user_id INT UNIQUE, first_name VARCHAR (255), "
#                   "last_name VARCHAR(255))")


# query = "INSERT INTO users(user_id, first_name, last_name) VALUES (%s, %s, %s)"
# values = (2, "Masha", "Ivanova")
# db_cursor.execute(query, values)
# db.commit()
#
# print(db_cursor.rowcount, 'запись добавлена. Пользоваель успешно '
#                           'зарегистрирован!')

user_data = {}


class User():
    def __init__(self, first_name):
        self.first_name = first_name
        self.last_name = ''


@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
    """ Первый шаг регистрации пользователя, вводится имя"""
    message = bot.send_message(msg.chat.id, 'Для регистрации введите ваше '
                                            'имя: ')
    bot.register_next_step_handler(message, process_firstname_step)


def process_firstname_step(msg):
    """ Второй шаг регистрации пользователя, вводится фамилия"""
    try:
        user_id = msg.from_user.id
        user_data[user_id] = User(msg.text)
        message = bot.send_message(msg.chat.id, 'Введите вашу фамилию: ')
        bot.register_next_step_handler(message, process_lastname_step)
    except Exception as e:
        bot.reply_to(msg, 'Что-то пошло не так, попробуйте снова '
                          '(возможно вы уже регистрировались ранее)')


def process_lastname_step(msg):
    """ Второй шаг регистрации пользователя: запись фамилии и сохранение
    информации о пользователе в БД"""
    try:
        user_id = msg.from_user.id
        user = user_data[user_id]
        user.last_name = msg.text

        query = "INSERT INTO users(user_id, first_name, last_name) " \
                "VALUES (%s, %s, %s)"
        values = (user_id, user.first_name, user.last_name)
        db_cursor.execute(query, values)
        db.commit()
        bot.send_message(msg.chat.id, 'Вы успешно зарегистрированы! ')
    except Exception as e:
        bot.reply_to(msg, 'Что-то пошло не так, попробуйте снова '
                          '(возможно вы уже регистрировались ранее)')


bot.enable_save_next_step_handlers(delay=2)

if __name__ == '__main__':
    bot.polling(none_stop=True)
