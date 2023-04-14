import telebot
from telebot import types
import cred


API_TOKEN = cred.token
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['menu'])
def welcome_text(message):
    keyboard = types.InlineKeyboardMarkup()
    buy_advertising = types.InlineKeyboardButton(text="💲 Купить рекламу на канале", callback_data='advertising')
    ask_button = types.InlineKeyboardButton(text='❓ Задать вопрос админам', callback_data='ask')
    offer_news = types.InlineKeyboardButton(text='🖐 Предложить пост в канал', callback_data='offer')
    keyboard.add(buy_advertising, ask_button, offer_news, row_width=1)
    bot.send_message(message.chat.id, text="Привет! Что тебя интересует? 🧐", reply_markup=keyboard)


def question_to_admins(message):
    receiver = cred.tg_id
    text = message.json['text']
    name = message.chat.username
    bot.send_message(chat_id=receiver, text=f'Вопрос от @{name}: {text}')
    bot.send_message(message.chat.id, text="""
            Спасибо за вопрос! ❤️
Ответ ждите в наших постах 

<i>Мы не гарантируем, что точно ответим на ваш вопрос. Возможно, на что-то подобное мы уже отвечали, либо вы затронули\
слишком личную тему.</i> """, parse_mode='HTML'
                     )


@bot.callback_query_handler(func=lambda callback: callback.data)
def callback_check(callback):
    if callback.data == 'advertising':
        bot.send_message(callback.message.chat.id, """Реклама в канале «Копилка текстов» стоит <b>4000 ₽</b>.

<b>Пост в ленте остаётся на 4 дня</b>, потом мы его удаляем. 

<b>Спустя 6 часов после публикации рекламы выпускаем второй пост</b> — обычно он короткий. При желании рекламодателя мы можем \
проконсультировать по рекламному посту. Это входит в стоимость рекламы

<b>Дату публикации бронируем после полной оплаты.</b>""", parse_mode='HTML')
        keyboard = types.InlineKeyboardMarkup()
        free_date = types.InlineKeyboardButton(
            text="📅 Свободные даты",
            callback_data='free_date',
            url='https://www.notion.so/fbeb2e0daca34e019021632062bad1d1'
        )
        buy = types.InlineKeyboardButton(text='💲 Купить рекламу ', callback_data='buy')
        back_bt = types.InlineKeyboardButton(text='В меню', callback_data='back')
        keyboard.add(free_date, buy, back_bt, row_width=1)
        bot.send_message(callback.message.chat.id,
                         text='Купить рекламу на канале (Можно переименовать)',
                         reply_markup=keyboard)
    elif callback.data == 'ask':
        bot.send_message(callback.message.chat.id,
                         text="""
                         Задайте нам, админам канала «Копилка текстов», интересующий вопрос. 

Приветствуются вопросы о том, как:

👀 писать тексты на разные темы, 
👀 коммуницировать с заказчиками, 
👀 развиваться в профессии. 

Также мы можем рассказать о своей работе, тайм-менеджменте, поделиться закулисьем канала. 

Напишите свой вопрос ниже 👇🏻
                         """
                         )

        bot.register_next_step_handler(callback.message, question_to_admins)

    elif callback.data == 'buy':
        bot.send_message(callback.message.chat.id, text="""
        Чтобы купить рекламу стучитесь к @lenka_napisaIa или к @isaewlad

Также мы открыты к взаимному пиару — подробности готовы обсуждать в личке.
        """)
    elif callback.data == 'back':
        welcome_text(callback.message)


if __name__ == '__main__':
    bot.infinity_polling()
