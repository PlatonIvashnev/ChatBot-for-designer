import telebot
from telebot import types
import webbrowser

bot = telebot.TeleBot('Token')
user_id_2 = 'Id'

user_steps = {}  # Dictionary path for user_1
user_images = {}  # Dictionary for image user_1

# Bot says HI after /start and show initial buttons
@bot.message_handler(commands=['start'])
def main_initial(message):
    user_steps[message.chat.id] = []
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Услуга 1', callback_data='service_1'))
    markup.add(types.InlineKeyboardButton('Услуга 2', callback_data='service_2'))
    markup.add(types.InlineKeyboardButton('Услуга 3', callback_data='service_3'))
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}', reply_markup=markup)

# Second set of buttons
def create_second_buttons():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Европа", callback_data='europe'))
    markup.add(types.InlineKeyboardButton("Россия", callback_data='russia'))
    markup.add(types.InlineKeyboardButton("Казахстан", callback_data='kazakhstan'))
    return markup

# Buttons for User2 confirmation
def create_confirmation_buttons():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Да", callback_data='yes'))
    markup.add(types.InlineKeyboardButton("Нет", callback_data='no'))
    return markup

# Buttons pushing handler
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data.startswith('service_'):
        step = f"Услуга {call.data[-1]}"
        user_steps[call.message.chat.id] = [step]
        bot.send_message(call.message.chat.id, f"Вот ваш заготовленный текст для {step}!", reply_markup=create_second_buttons())
    elif call.data in ['europe', 'russia', 'kazakhstan']:
        step = 'Европа' if call.data == 'europe' else 'Россия' if call.data == 'russia' else 'Казахстан'
        user_steps[call.message.chat.id].append(step)
        bot.send_message(call.message.chat.id, f"Вы выбрали {step}. Пожалуйста, отправьте изображение.")
    elif call.data in ['yes', 'no']:
        # Логирование для отладки
        print(f"Received {call.data} from user_id_2")
        user_image_info = user_images.get(user_id_2, None)

        if user_image_info:
            if call.data == 'yes':
                bot.send_message(user_image_info['from'], "Ваше изображение принято. Вот ссылка: [http://vassagraphicdesign.tilda.ws/]")
            else:
                bot.send_message(user_image_info['from'], "Извините, ваше изображение отклонено.")
            bot.send_message(call.message.chat.id, "Ваш ответ был передан.")
        else:
            # Логирование для отладки
            print("User image info not found.")

# Image handler
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.chat.id in user_steps and user_steps[message.chat.id][-1] in ['Европа', 'Россия', 'Казахстан']:
        photo_id = message.photo[-1].file_id
        user_images[user_id_2] = {'from': message.chat.id, 'steps': user_steps[message.chat.id], 'photo_id': photo_id}
        try:
            bot.send_photo(user_id_2, photo_id, caption=f"Пользователь прошел путь {' - '.join(user_steps[message.chat.id])}. Примите изображение?", reply_markup=create_confirmation_buttons())
            bot.send_message(message.chat.id, "Ваше изображение отправлено на проверку.")
        except telebot.apihelper.ApiTelegramException as e:
            bot.send_message(message.chat.id, f"Ошибка отправки изображения: {e}")

def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')


bot.polling(non_stop=True)