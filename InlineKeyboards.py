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

def tap_to_connect():
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
