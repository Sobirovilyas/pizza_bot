from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import sqlite3
from constants import get_products_query, create_new_user_query

TOKEN = '5943242364:AAEDa7ko4pgcCKnzSOw7WdvU8eYMH8OWD6M'

bot = TeleBot(TOKEN, parse_mode=None)


def main_menu_keyboard():
    """
    Эта функция создает первоначальное меню в нашем телаграм боте.

    :return: Объект класса ReplyKeyboardMarkup
    """

    cart = KeyboardButton("Корзина")
    menu = KeyboardButton("Меню")

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(menu)
    keyboard.add(cart)

    return keyboard


def get_product_names() -> list:
    products = []

    try:
        conn = sqlite3.connect("pizza_database.db")
        cursor = conn.cursor()
        sql = get_products_query()
        cursor.execute(sql)

        for product in cursor.fetchall():
            products.append(product[0])

    except Exception as e:
        print(e)

    return products
def menu_keyboard():
    """
    Это меню высвечивает товары в нашей базе данных

    :return: Объект класса ReplyKeyboardMarkup
    """

    products = get_product_names()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    row = []
    for product in products:
        button = KeyboardButton(product)
        row.append(button)
        if len(row) == 2:
            keyboard.add(*row)
            row = []

    if row:
        keyboard.add(*row)
    back_button = KeyboardButton("<< Назад")

    keyboard.add(back_button)

    return keyboard


def get_user_details_keyboard():

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    get_phone_button = KeyboardButton("Ввести номер телефона")
    get_address_button = KeyboardButton("Ввести адрес")

    keyboard.add(get_phone_button)
    keyboard.add(get_address_button)

    return keyboard


def create_user(chat_id):

    try:
        conn = sqlite3.connect('pizza_database.db')
        cursor = conn.cursor()
        sql = create_new_user_query(chat_id)
        cursor.execute(sql)

    except Exception as e:
        print(e)



@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id

    create_user(chat_id)

    reply = "Вас приветствует бот доставки пиццы."
    bot.reply_to(message, reply, reply_markup=get_user_details_keyboard())


@bot.message_handler(func=lambda message: message.text == 'Меню')
def menu_handler(message):
    reply = "Выберите пиццу:"
    bot.reply_to(message, reply, reply_markup=menu_keyboard())


bot.infinity_polling()
