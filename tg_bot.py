import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import logger_config
from time_declination_funcs import time_left

import InlineKeyboards
import MarzbanController


# Настройка логгера
root_logger = logger_config.setup_logger()

BOT_TOKEN = os.getenv('TG_TOKEN')
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    msg = await bot.send_message(
        chat_id=message.from_user.id,
        text='<b>Привет!</b> 🚀 \n\nЯ <b>бот для продажи VPN</b>\n\nКаждому новому пользователю доступен пробный период - 3 дня.',
        parse_mode='HTML',
        reply_markup=InlineKeyboards.start()
    )
    await state.update_data(message_id=msg.message_id)


@dp.callback_query(lambda F: F.data == 'start')
async def start_edited(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    msg = await callback.bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=message_id,
        text='<b>Привет!</b> 🚀 \n\nЯ <b>бот для продажи VPN</b>',
        parse_mode='HTML',
        reply_markup=InlineKeyboards.start()
    )
    await state.update_data(message_id=msg.message_id)


@dp.callback_query(lambda F: F.data == 'status')
async def status(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    expire = await controller.get_expire(str(callback.from_user.id))
    text = time_left(expire)
    if expire > 0 or expire is True:
        msg = await callback.bot.edit_message_text(
            chat_id=callback.from_user.id,
            message_id=message_id,
            text=text,
            parse_mode='HTML',
            reply_markup=InlineKeyboards.back()
        )
        await state.update_data(message_id=msg.message_id)
    else:
        msg = await callback.bot.edit_message_text(
            chat_id=callback.from_user.id,
            message_id=message_id,
            text=text,
            parse_mode='HTML',
            reply_markup=InlineKeyboards.expired()
        )
        await state.update_data(message_id=msg.message_id)


@dp.callback_query(lambda F: F.data == 'connect')
async def connect(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    if await controller.add_user(str(callback.from_user.id), 3):
        msg = await callback.bot.edit_message_text(
            chat_id=callback.from_user.id,
            message_id=message_id,
            text='Вы активировали пробный период - 3 дня, внимание на кнопки ниже',
            parse_mode='HTML',
            reply_markup=InlineKeyboards.to_connect()
        )
        await state.update_data(message_id=msg.message_id)
    else:
        expire = await controller.get_expire(str(callback.from_user.id))
        text = time_left(expire)
        msg = await callback.bot.edit_message_text(
            chat_id=callback.from_user.id,
            message_id=message_id,
            text=text,
            parse_mode='HTML',
            reply_markup=InlineKeyboards.to_connect() if expire > 0 else InlineKeyboards.expired()
        )
        await state.update_data(message_id=msg.message_id)


@dp.callback_query(lambda F: F.data == 'buy')
async def buy(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    msg = await callback.bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=message_id,
        text='Менюшка покупки',
        parse_mode='HTML',
        reply_markup=InlineKeyboards.buy()
    )
    await state.update_data(message_id=msg.message_id)


@dp.callback_query(lambda F: F.data == 'one_month')
async def one_month(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    msg = await callback.bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=message_id,
        text='Подписка - 1 месяц',
        parse_mode='HTML',
        reply_markup=InlineKeyboards.one_month()
    )
    await state.update_data(message_id=msg.message_id)


@dp.callback_query(lambda F: F.data == 'three_months')
async def three_months(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    msg = await callback.bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=message_id,
        text='Подписка - 3 месяца',
        parse_mode='HTML',
        reply_markup=InlineKeyboards.three_months()
    )
    await state.update_data(message_id=msg.message_id)


@dp.callback_query(lambda F: F.data == 'six_months')
async def six_months(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    msg = await callback.bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=message_id,
        text='Подписка - 6 месяцев',
        parse_mode='HTML',
        reply_markup=InlineKeyboards.six_months()
    )
    await state.update_data(message_id=msg.message_id)


@dp.callback_query(lambda F: F.data == 'help')
async def get_help(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    msg = await callback.bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=message_id,
        text='Для получения помощи напишите сюда ...',
        parse_mode='HTML',
        reply_markup=InlineKeyboards.back()
    )
    await state.update_data(message_id=msg.message_id)


@dp.callback_query(lambda F: F.data == 'payment_confirmed')
async def payment_confirmed(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')

    expire = await controller.get_expire(str(callback.from_user.id))
    if expire is True:
        text = 'У вас безлимит'
    elif expire > 0:
        text = 'Оплата прошла успешно, вам добавлен 1 месяц'
        await controller.add_expire(str(callback.from_user.id), 30)
    else:
        text = 'Оплата прошла успешно, вам выдан 1 месяц'
        await controller.update_expire(str(callback.from_user.id), 30)
    msg = await callback.bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=message_id,
        text=text,
        parse_mode='HTML',
        reply_markup=InlineKeyboards.payment_confirmed()
    )
    await state.update_data(message_id=msg.message_id)


async def main():
    global controller
    token = await MarzbanController.api.get_token(username=os.getenv('MARZBAN_USERNAME'), password=os.getenv('MARZBAN_PASSWORD'))
    controller = MarzbanController.Controller(token)
    root_logger.info('Бот начал работу')
    await dp.start_polling(bot)


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
asyncio.run(main())
