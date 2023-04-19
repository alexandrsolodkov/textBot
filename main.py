import telebot
from telebot import types
import cred
import text_message
from datetime import datetime


API_TOKEN = cred.token
bot = telebot.TeleBot(API_TOKEN)
receiver = cred.tg_id
press_button = False


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
    offer_vacancy = types.InlineKeyboardButton(text=text_message.offer_vacancy, callback_data='vacancy')
    ask_button = types.InlineKeyboardButton(text=text_message.ask_button, callback_data='ask')
    offer_news = types.InlineKeyboardButton(text=text_message.offer_news, callback_data='offer')
    keyboard.add(buy_advertising, offer_vacancy, ask_button, offer_news, row_width=1)
    bot.send_message(message.chat.id, text=text_message.welcome_text, reply_markup=keyboard)


def offer_vacancy_act(message):
    global press_button
    try:
        bot.forward_message(receiver, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, text=text_message.vacancy_answer, parse_mode='HTML')
        press_button = False
    except KeyError:
        bot.send_message(message.chat.id, text=text_message.not_text)


def question_to_admins(message):
    global press_button
    try:
        bot.forward_message(receiver, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, text=text_message.question_to_admin, parse_mode='HTML')
        press_button = False
    except KeyError:
        bot.send_message(message.chat.id, text=text_message.not_text)


def take_news(message):
    global press_button
    try:
        bot.forward_message(receiver, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, text=text_message.thnx_message)
        press_button = False
    except KeyError:
        bot.send_message(message.chat.id, text=text_message.not_news)


@bot.callback_query_handler(func=lambda callback: callback.data == 'advertising')
def callback_advertising(callback):
    bot.send_message(
        callback.message.chat.id,
        text=text_message.advertising,
        parse_mode='HTML',
        disable_web_page_preview=True
    )


@bot.callback_query_handler(func=lambda callback: callback.data == 'vacancy')
def callback_vacancy(callback):
    global press_button
    if not press_button:
        press_button = True
        bot.send_message(
            callback.message.chat.id,
            text=text_message.vacancy_description,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
        bot.register_next_step_handler(callback.message, offer_vacancy_act)
    else:
        return


@bot.callback_query_handler(func=lambda callback: callback.data == 'ask')
def callback_ask(callback):
    global press_button
    if not press_button:
        press_button = True
        bot.send_message(callback.message.chat.id, text=text_message.ask)
        bot.register_next_step_handler(callback.message, question_to_admins)
    else:
        return


@bot.callback_query_handler(func=lambda callback: callback.data == 'offer')
def callback_offer(callback):
    global press_button
    if not press_button:
        press_button = True
        bot.send_message(callback.message.chat.id, text=text_message.offer_text)
        bot.register_next_step_handler(callback.message, take_news)
    else:
        return


if __name__ == '__main__':
    bot.infinity_polling()
