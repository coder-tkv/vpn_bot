from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start():
    start_buttons_list = [
        [InlineKeyboardButton(text="Статус", callback_data='status')],
        [InlineKeyboardButton(text="Подключиться", callback_data='connect')],
        [InlineKeyboardButton(text="Купить", callback_data='buy')],
        [InlineKeyboardButton(text="Помощь", callback_data='help')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=start_buttons_list)

def back():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data='start')]])

def to_connect():
    connect_buttons_list = [
        [
            InlineKeyboardButton(text="Скачать Android", callback_data='download_android'),
            InlineKeyboardButton(text="Подключить Android", callback_data='connect_android')
        ],
        [
            InlineKeyboardButton(text="Скачать iOS", callback_data='download_ios'),
            InlineKeyboardButton(text="Подключить iOS", callback_data='connect_ios')
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data='start')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=connect_buttons_list)

def expired():
    expired_buttons_list = [
        [InlineKeyboardButton(text="Купить", callback_data='buy')],
        [InlineKeyboardButton(text="Назад", callback_data='start')]]
    return InlineKeyboardMarkup(inline_keyboard=expired_buttons_list)


def buy():
    buy_buttons_list = [
        [InlineKeyboardButton(text="1 месяц", callback_data='one_month')],
        [InlineKeyboardButton(text="3 месяца", callback_data='three_months')],
        [InlineKeyboardButton(text="6 месяцев", callback_data='six_months')],
        [InlineKeyboardButton(text="Назад", callback_data='start')]]
    return InlineKeyboardMarkup(inline_keyboard=buy_buttons_list)


def one_month():
    one_month_buttons_list = [
        [InlineKeyboardButton(text="Оплатить", callback_data='123')],
        [InlineKeyboardButton(text="Криптой", callback_data='123')],
        [InlineKeyboardButton(text="Назад", callback_data='buy')]]
    return InlineKeyboardMarkup(inline_keyboard=one_month_buttons_list)


def three_months():
    three_months_buttons_list = [
        [InlineKeyboardButton(text="Оплатить", callback_data='123')],
        [InlineKeyboardButton(text="Криптой", callback_data='123')],
        [InlineKeyboardButton(text="Назад", callback_data='buy')]]
    return InlineKeyboardMarkup(inline_keyboard=three_months_buttons_list)


def six_months():
    six_months_buttons_list = [
        [InlineKeyboardButton(text="Оплатить", callback_data='123')],
        [InlineKeyboardButton(text="Криптой", callback_data='123')],
        [InlineKeyboardButton(text="Назад", callback_data='buy')]]
    return InlineKeyboardMarkup(inline_keyboard=six_months_buttons_list)