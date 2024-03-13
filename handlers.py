import logging

from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters.command import Command

from api_requests import get_api_answer
from constants import DB_MSG, INFO_MSG
from crud import requests_info_crud

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.text, Command("start"))
async def start_handler(msg: Message):
    logger.info(f"Получено сообщение {msg.text}")
    await msg.answer("Command start!")


@router.message(F.text, Command("get"))
async def get_handler(msg: Message):
    logger.info(f"Получено сообщение {msg.text}")
    objs = await requests_info_crud.get(msg.from_user.id)
    message = ""
    for obj in objs:
        message += DB_MSG.format(obj.create_date, obj.article)
    await msg.answer(message)


@router.message(F.text)
async def message_handler(msg: Message):
    logger.info(f"Получено сообщение {msg.text}")
    await msg.answer(INFO_MSG.format(*get_api_answer(int(msg.text))))
    info = dict(user_id=int(msg.from_user.id), article=int(msg.text))
    await requests_info_crud.create(info)
