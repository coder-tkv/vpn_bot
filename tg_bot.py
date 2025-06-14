import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import InlineKeyboards
import MarzbanController

BOT_TOKEN = os.getenv('TG_TOKEN')
dp = Dispatcher()
controller = None

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
    msg = await callback.bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=message_id,
        text='status',
        parse_mode='HTML',
        reply_markup=InlineKeyboards.back()
    )
    await state.update_data(message_id=msg.message_id)

@dp.callback_query(lambda F: F.data == 'connect')
async def connect(callback: CallbackQuery, state: FSMContext):
    if await controller.add_user(str(callback.from_user.id), 3):
        data = await state.get_data()
        message_id = data.get('message_id')
        msg = await callback.bot.edit_message_text(
            chat_id=callback.from_user.id,
            message_id=message_id,
            text='Вы активировали пробный период - 3 дня, внимание на кнопки ниже',
            parse_mode='HTML',
            reply_markup=InlineKeyboards.tap_to_connect()
        )
        await state.update_data(message_id=msg.message_id)
    else:
        # добавить функцию получения времени
        pass


async def main():
    global controller
    token = await MarzbanController.api.get_token(username=os.getenv('MARZBAN_USERNAME'), password=os.getenv('MARZBAN_PASSWORD'))
    controller = MarzbanController.Controller(token)
    await dp.start_polling(bot)


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
asyncio.run(main())