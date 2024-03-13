import telebot
from telebot import types
import re

TOKEN = '6546041003:AAEsgIiWyN991C3kl_GJ_tc6BzSA_RK-H-E'

bot = telebot.TeleBot(TOKEN)

phone_number_regex = re.compile(r'^(\+7|8)\d{10}$')
age_regex = re.compile(r'^\d.*')
district_regex = re.compile(r'^\D.*')
data = {}
request_chat_id = '-1002088344075'

@bot.message_handler(commands=['start'])

def enter_district(message):
    clear_data(message)
    data[message.chat.id] = {'stage':0}
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text='Центр', callback_data='Центр')
    itembtn2 = types.InlineKeyboardButton(text='ВИЗ', callback_data='ВИЗ')
    itembtn3 = types.InlineKeyboardButton(text='Ботаника', callback_data='Ботаника')
    itembtn4 = types.InlineKeyboardButton(text='Академический', callback_data='Академический')
    
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_photo(message.chat.id, open('kiber1.png', 'rb'))
    bot.send_message(message.chat.id, 'Школа программирования для детей KIBERone Екатеринбург приветствует вас!\U0001F60A\n \nДля летних КИБЕРканикул мы подготовили для Вас 6 уникальных модулей, которые разработали на основе самых актуальных и трендовых тенденций IT-образования\U0001F4BB\n \n\U00002705Minecraft и таинственный портал (8+);\n \n\U00002705Создай свою карту в Roblox Studio (8+);\n \n\U00002705Новый Марио на Construct (8+);\n \n\U00002705Магия нейросетей. Курс искусственного интеллекта в помощь ребенку (8+);\n \n\U00002705Делаем супер-сайты со спецэффектами. Анимация в Figma (11+);\n \n\U00002705Создание интерактивной игры с собственном персонажем на конструкторе ClickTeam Fusion (11+).\n \nВыберите удобный для Вас район\U0001F447' , reply_markup=markup)
    
def enter_age(message):
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text='8-10 лет', callback_data='8-10')
    itembtn2 = types.InlineKeyboardButton(text='11-14 лет', callback_data='11-14')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, 'Пожалуйста, укажите возраст вашего ребенка\U0001F447',reply_markup=markup)


def enter_phone_number(message):
    bot.send_message(message.chat.id, 'Спасибо! Остался последний шаг\U0001F60A\n \nПожалуйста, введите номер телефона, по которому мы можем с Вами связаться\U0001F4F1')
    
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text.startswith('/start'):
        return
    if message.text.startswith('/getID'):
        bot.send_message(message.chat.id, message.chat.id)
        return
    if message.text.startswith('/'):
        bot.send_message(message.chat.id, 'Неверная команда')
        return
    if phone_number_regex.match(message.text) and data[message.chat.id]['stage'] == 2:
        data[message.chat.id]['phone_number'] = message.text
        data[message.chat.id]['stage'] = 3
        check_and_send(message)
        return
    else:
        bot.send_message(message.chat.id, 'Повторите попытку')
        return

def check_and_send(message):
    if district_regex.match(data[message.chat.id]['district']) and age_regex.match(data[message.chat.id]['age']):
        bot.send_message(message.chat.id, 'Спасибо! Скоро с Вами свяжется наш менеджер и подберёт подходящую смену для Вашего ребёнка. \n \nДо встречи на летних КИБЕРканикулах!\U0001F60A')
        bot.send_message(request_chat_id, '\U00002757\U00002757\U00002757 Новый лид\U00002757\U00002757\U00002757'+'\nРайон: ' + data[message.chat.id]['district']+'\nВозраст: '+data[message.chat.id]['age']+'\nТел: '+data[message.chat.id]['phone_number'])
        clear_data(message)
    else:
        bot.send_message(message.chat.id, 'Неправильно сформированы ответы на вопросы, поробуйте еще раз')
        enter_district(message)
    
def clear_data(message):
    if message.chat.id in data:
        del data[message.chat.id]
  
@bot.callback_query_handler(func=lambda call: True)
def answering(call):
    if call.message.chat.id in data:
        if data[call.message.chat.id]['stage'] == 0:
            data[call.message.chat.id]['district'] = call.data
            data[call.message.chat.id]['stage'] = 1
            enter_age(call.message)
        elif data[call.message.chat.id]['stage'] == 1:
            data[call.message.chat.id]['age'] = call.data
            data[call.message.chat.id]['stage'] = 2
            enter_phone_number(call.message)
bot.infinity_polling()
