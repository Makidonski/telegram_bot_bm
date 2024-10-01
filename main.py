import telebot
from pymongo import MongoClient
import const_helper
import messages
from telebot import types
import db_helpers
import uuid

# Инициализация бота
bot = telebot.TeleBot(const_helper.TOKEN)
print('Бот работает')

@bot.message_handler(commands=[const_helper.COMMANDS['START']])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(messages.GET_ORDERS))
    markup.add(types.KeyboardButton(const_helper.COMMANDS['ANSWER_CLIENTS']))

    bot.send_message(
        message.chat.id,
        messages.WELCOME.format(message.from_user, bot.get_me()),
        parse_mode='html',
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == const_helper.COMMANDS['GET_CLIENTS'])
def get_clients(message):
    clients = db_helpers.get_clients()

    message_with_client = f'{messages.UNHANDLED_ORDERS}' 
    for client in clients:
        name = client['name']
        contact = client['contact']
        products = client['products']
        message_for_client = f'\n{messages.NAME}: {name}\n{messages.CONTACT}: {contact} \n{messages.ORDERED_GOODS}:\n' 
        for product in products:
            message_for_client = message_for_client + f' - {product['category_name']}: {product['price']} \n \n'

        message_with_client = message_with_client + message_for_client
    bot.send_message(
        message.chat.id,
        message_with_client.format(message.from_user, bot.get_me()),
        parse_mode='html',
    )

@bot.message_handler(func=lambda message: message.text == const_helper.COMMANDS['ANSWER_CLIENTS'])
def answer_client(message):
    clients = db_helpers.get_clients()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for client in clients:
        name = client['name']
        contact = client['contact']
        button_message_for_client = f'{messages.ANSWER} {name}: {contact}' 
        markup.add(types.KeyboardButton(button_message_for_client))

    bot.send_message(
        message.chat.id,
        f'{messages.CLICK_ON}', 
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: const_helper.COMMANDS['ANSWER'] in message.text)
def answer(message):
    client_contact = message.text.split(': ')[1]
    db_helpers.answer_client(client_contact)
    bot.send_message(
        message.chat.id,
        'Нажмите на клиента, которому вы уже ответили',
    )
bot.polling(none_stop=True)