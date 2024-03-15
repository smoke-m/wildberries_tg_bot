"""Модуль Хендлеров проекта."""

import asyncio
import logging
import re

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from api_requests import get_api_answer
from constants import ARTICLE_PAT, ARTICLE_RE, DB_MSG, INFO_MSG, TIME_SPAM
from crud import requests_info_crud
from keyboards import keyboard_main, keyboard_inline

logger = logging.getLogger(__name__)
router = Router()
spam_arr = set()


class MyState(StatesGroup):
    """Класс состояния."""

    get_article = State()


@router.message(F.text, Command("start"))
async def start_handler(msg: Message):
    """Хендлер старта работы с пользователем."""
    logger.info(f"Получено сообщение {msg.text}")
    await msg.answer("Дабро пожаловать!", reply_markup=keyboard_main)


@router.message(F.text.lower() == "получить информацию из бд")
async def get_handler(msg: Message):
    """Хендлер возвращает информацию из базы."""
    logger.info(f"Получено сообщение {msg.text}")
    objs = await requests_info_crud.get(msg.from_user.id)
    message = ""
    for obj in objs:
        message += DB_MSG.format(obj.create_date, obj.article)
    await msg.answer(message)


@router.callback_query(F.data == "spam")
async def start_spam(callback: CallbackQuery):
    """Хендлер отправляет информацию по товару раз в 5 мин."""
    logger.info(f"Получено сообщение!!! {callback.message.text}")
    spam_arr.add(callback.from_user.id)
    article = re.search(ARTICLE_RE, callback.message.text).group(1)
    await callback.answer(text="Подписка на товар подключена", show_alert=True)
    try:
        while callback.from_user.id in spam_arr:
            await callback.message.answer(
                INFO_MSG.format(*get_api_answer(int(article))),
            )
            info = dict(
                user_id=int(callback.from_user.id), article=int(article)
            )
            await requests_info_crud.create(info)
            await asyncio.sleep(TIME_SPAM)
    except Exception as error:
        logger.critical(error)
        await callback.message.answer("Ошибка сервера!")


@router.message(F.text.lower() == "остановить уведомления")
async def stop_spam(msg: Message):
    """Хендлер останавливает опраку сообщений."""
    logger.info(f"Получено сообщение {msg.text}")
    spam_arr.discard(msg.from_user.id)


@router.message(F.text.lower() == "получить информацию по товару")
async def get_info(msg: Message, state: FSMContext):
    """Хендлер запуска состояния получить артикул."""
    logger.info(f"Получено сообщение {msg.text}")
    await msg.answer("Введите артикул товара:")
    await state.set_state(MyState.get_article)


@router.message(MyState.get_article)
async def return_info(msg: Message, state: FSMContext):
    """Хендлер выдачи информации о товаре."""
    logger.info(f"Получено сообщение {msg.text}")
    if re.compile(ARTICLE_PAT).match(msg.text):
        try:
            await msg.answer(
                INFO_MSG.format(*get_api_answer(int(msg.text))),
                reply_markup=keyboard_inline,
            )
            info = dict(user_id=int(msg.from_user.id), article=int(msg.text))
            await requests_info_crud.create(info)
        except Exception as error:
            logger.critical(error)
            await msg.answer("Ошибка сервера!")
    else:
        await msg.answer("Введён не корректный артикул!")
    await state.clear()
