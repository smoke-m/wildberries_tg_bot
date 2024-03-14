import asyncio
import logging

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command

from api_requests import get_api_answer
from constants import DB_MSG, INFO_MSG
from crud import requests_info_crud
from keyboards import keyboard_main, keyboard_inline

logger = logging.getLogger(__name__)
router = Router()
spam_arr = set()


@router.message(F.text, Command("start"))
async def start_handler(msg: Message):
    logger.info(f"Получено сообщение {msg.text}")
    await msg.answer("Command start!", reply_markup=keyboard_main)


@router.message(F.text.lower() == "получить информацию из бд")
async def get_handler(msg: Message):
    logger.info(f"Получено сообщение {msg.text}")
    objs = await requests_info_crud.get(msg.from_user.id)
    message = ""
    for obj in objs:
        message += DB_MSG.format(obj.create_date, obj.article)
    await msg.answer(message)


@router.callback_query(F.data == "spam")
async def start_spam(callback: CallbackQuery):
    logger.info(f"Получено сообщение!!! {callback.message.text}")
    spam_arr.add(callback.from_user.id)
    await callback.answer(text="Подключено", show_alert=True)
    while callback.from_user.id in spam_arr:
        await asyncio.sleep(15)
        await callback.message.answer("Command spam")


@router.message(F.text.lower() == "остановить уведомления")
async def stop_spam(msg: Message):
    logger.info(f"Получено сообщение {msg.text}")
    spam_arr.discard(msg.from_user.id)


@router.message(F.text)
async def message_handler(msg: Message):
    logger.info(f"Получено сообщение {msg.text}")
    await msg.answer(
        INFO_MSG.format(*get_api_answer(int(msg.text))),
        reply_markup=keyboard_inline,
    )
    info = dict(user_id=int(msg.from_user.id), article=int(msg.text))
    await requests_info_crud.create(info)
