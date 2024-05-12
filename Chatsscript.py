import telebot

bot = telebot.TeleBot('7159383606:AAEtWZ_TEQBWAM2STMO4PdP4_Aanhis8hYQ')
@bot.message_handler(commands=['start'])

def main(message):
    bot.send_message(message.chat.id, 'Доброго дня')

bot.polling(non_stop=True)