import telebot
from telebot import types
import webbrowser

bot = telebot.TeleBot('7159383606:AAEtWZ_TEQBWAM2STMO4PdP4_Aanhis8hYQ')

@bot.message_handler(commands=['start'])


def main(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Услуга 1', text='Дескрипшн 1 и 100'))
    markup.add(types.InlineKeyboardButton('Услуга 2', text='Дескрипшн 2 и 200'))
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}', reply_markup=markup)


def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')


bot.polling(non_stop=True)