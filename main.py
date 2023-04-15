import telebot
from telebot import types
import cred
import text_message
from datetime import datetime


API_TOKEN = cred.token
bot = telebot.TeleBot(API_TOKEN)
receiver = cred.tg_id


@bot.message_handler(commands=['start'])
def start_stat(message):
    with open(file='statistics/activation_stat.txt', mode='a') as pc:
        full_name = message.from_user.full_name
        user_name = message.from_user.username
        user_id = message.from_user.id
        usage_time = datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S')
        pc.write(f'{user_id}|{full_name}|{user_name}|{usage_time}' + '\n')
    welcome_text(message)


# main menu
@bot.message_handler(commands=['menu'])
def welcome_text(message):
    keyboard = types.InlineKeyboardMarkup()
    buy_advertising = types.InlineKeyboardButton(text=text_message.buy_advertising, callback_data='advertising')
    ask_button = types.InlineKeyboardButton(text=text_message.ask_button, callback_data='ask')
    offer_news = types.InlineKeyboardButton(text=text_message.offer_news, callback_data='offer')
    keyboard.add(buy_advertising, ask_button, offer_news, row_width=1)
    bot.send_message(message.chat.id, text=text_message.welcome_text, reply_markup=keyboard)


def ask_admin(message):
    bot.register_next_step_handler(message, question_to_admins)


def question_to_admins(message):
    try:
        bot.forward_message(receiver, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, text=text_message.question_to_admin, parse_mode='HTML')
    except KeyError:
        bot.send_message(message.chat.id, text=text_message.not_text)
        ask_admin(message)


def take_news(message):
    try:
        bot.forward_message(receiver, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, text=text_message.thnx_message)
    except KeyError:
        bot.send_message(message.chat.id, text=text_message.not_news)
        ask_admin(message)


@bot.callback_query_handler(func=lambda callback: callback.data)
def callback_check(callback):

    if callback.data == 'advertising':
        keyboard = types.InlineKeyboardMarkup()
        free_date = types.InlineKeyboardButton(
            text=text_message.free_date,
            callback_data='free_date',
            url='https://www.notion.so/fbeb2e0daca34e019021632062bad1d1'
        )
        buy = types.InlineKeyboardButton(text=text_message.buy_bt, callback_data='buy')
        back_bt = types.InlineKeyboardButton(text=text_message.back_bt, callback_data='back')
        keyboard.add(free_date, buy, back_bt, row_width=2)
        bot.send_message(
            callback.message.chat.id,
            text=text_message.advertising,
            parse_mode='HTML',
            reply_markup=keyboard
        )

    elif callback.data == 'ask':
        bot.send_message(callback.message.chat.id, text=text_message.ask)
        ask_admin(callback.message)

    elif callback.data == 'buy':
        bot.send_message(callback.message.chat.id, text=text_message.buy_text)

    elif callback.data == 'offer':
        bot.send_message(callback.message.chat.id, text=text_message.offer_text)
        bot.register_next_step_handler(callback.message, take_news)

    elif callback.data == 'back':
        welcome_text(callback.message)


if __name__ == '__main__':
    bot.infinity_polling()
