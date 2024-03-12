import logging

from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters.command import Command

from crud import requests_info_crud

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.text, Command("start"))
async def start_handler(msg: Message):
    logger.info(f"Получено сообщение {msg.text}")
    await msg.answer("Command start!")


@router.message(F.text, Command("get"))
async def get_handler(msg: Message):
    obj = await requests_info_crud.get(msg.from_user.id)
    logger.info(f"Получено сообщение {msg.text}")
    await msg.answer(f"ID user {obj.user_id}\n" f"Текст: {obj.article}")


@router.message(F.text)
async def message_handler(msg: Message):
    logger.info(f"Получено сообщение {msg.text}")
    await msg.answer(f"ID: {msg.from_user.id}\n" f"Текст: {msg.text}")
    info = dict(user_id=msg.from_user.id, article=msg.text)
    await requests_info_crud.create(info)
