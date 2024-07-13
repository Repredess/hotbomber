import requests
import time
import telebot
from telebot import types
from DATA import BOT_TOKEN

bomber_bot = telebot.TeleBot(BOT_TOKEN)


@bomber_bot.message_handler(commands=["start"])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bomber_bot.send_message(message.chat.id,
                            f"БОМБИТ!!!",
                            parse_mode='html', reply_markup=markup)

def go_infinity():
    print("some troubles with network")
    try:
        # https://stackoverflow.com/questions/68739567/socket-timeout-on-telegram-bot-polling
        bomber_bot.infinity_polling(timeout=10, long_polling_timeout=5)
        bomber_bot.send_message(message_chat.id, "Проблемы с сервером... Подождите минутку")
        # pennij_bot.polling(none_stop=True)
    except requests.exceptions.ConnectionError:
        bomber_bot.infinity_polling(timeout=10, long_polling_timeout=5)
    time.sleep(5)


try:
    # https://stackoverflow.com/questions/68739567/socket-timeout-on-telegram-bot-polling
    bomber_bot.infinity_polling(timeout=10, long_polling_timeout=5)
except requests.exceptions.ConnectionError:
    print("Траблы ConnectionError")
    bomber_bot.infinity_polling(timeout=10, long_polling_timeout=5)
except requests.exceptions.ReadTimeout:
    print("Траблы ReadTimeout")
    bomber_bot.infinity_polling(timeout=10, long_polling_timeout=5)
except telebot.apihelper.ApiTelegramException:
    print("Траблы ReadTimeout")
    bomber_bot.infinity_polling(timeout=10, long_polling_timeout=5)