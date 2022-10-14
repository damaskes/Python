import telebot
from telebot import types

import data
from terms import *
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
game_data = data.Data()
current_data = game_data.get_current_data()


def create_markup():
    global current_data
    markup = types.InlineKeyboardMarkup()
    for button in current_data.get(BUTTONS):
        item = types.InlineKeyboardButton(text=button.get(BUTTON_TEXT), callback_data=button.get(BUTTON_ID))
        markup.add(item)
    return markup


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = create_markup()
    bot.send_message(message.chat.id, current_data.get(QUEST_TEXT), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def speak(message):
    global game_data, current_data
    current_data = game_data.get_current_data()
    markup = create_markup()
    bot.send_message(message.chat.id, current_data.get(QUEST_TEXT), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global current_data
    try:
        buttons_values = []
        for button in current_data.get(BUTTONS):
            buttons_values.append(button.get(BUTTON_ID))
        if call.message:
            if call.data in buttons_values:
                game_data.set_data_id(call.data)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=call.message.text, reply_markup=None)
            speak(call.message)
    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
