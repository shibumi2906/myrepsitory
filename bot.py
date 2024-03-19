import telebot
import threading
import time
from telebot import types

TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(TOKEN)

users_chat_id = set()  # Множество для хранения chat_id всех пользователей
reminders = {}  # chat_id: [list of reminders]
feedbacks = {}  # chat_id: feedback

def send_reminders():
    while True:
        current_time = time.strftime("%H:%M")
        for chat_id, times in reminders.items():
            if current_time in times:
                bot.send_message(chat_id, "Напоминание - выпей стакан воды")
        time.sleep(60)  # Проверяем каждую минуту

@bot.message_handler(commands=['start'])
def start_message(message):
    users_chat_id.add(message.chat.id)
    bot.reply_to(message, 'Привет! Я чат-бот, который будет напоминать тебе пить водичку! Используй команды /setreminder для настройки напоминаний и /feedback для обратной связи.')

@bot.message_handler(commands=['setreminder'])
def set_reminder(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('09:00', '14:00', '18:00')  # Примерные времена для напоминаний
    msg = bot.reply_to(message, 'Выберите время для напоминания или введите своё (в формате HH:MM)', reply_markup=markup)
    bot.register_next_step_handler(msg, process_reminder_time)

def process_reminder_time(message):
    chat_id = message.chat.id
    time = message.text
    if chat_id not in reminders:
        reminders[chat_id] = []
    reminders[chat_id].append(time)
    bot.send_message(chat_id, f'Напоминание установлено на {time}')

@bot.message_handler(commands=['feedback'])
def feedback(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Отлично', 'Хорошо', 'Пойдет', 'Плохо')
    msg = bot.reply_to(message, 'Как бы вы оценили нашего бота?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_feedback)

def process_feedback(message):
    chat_id = message.chat.id
    feedback = message.text
    feedbacks[chat_id] = feedback
    bot.send_message(chat_id, 'Спасибо за ваш отзыв!')

# Запускаем отдельный поток для функции отправки напоминаний
reminder_thread = threading.Thread(target=send_reminders)
reminder_thread.start()

# Запускаем бота
bot.polling(none_stop=True)