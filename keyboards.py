"""Модуль создания клавиатур."""

from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


buttons = [
    [KeyboardButton(text="Получить информацию по товару")],
    [KeyboardButton(text="Получить информацию из БД")],
    [KeyboardButton(text="Остановить уведомления")],
]

buttons_inline = [
    [InlineKeyboardButton(text="подписаться", callback_data="spam")]
]

keyboard_main = ReplyKeyboardMarkup(
    keyboard=buttons,
    resize_keyboard=True,
    input_field_placeholder="Выберите что надо сделать",
)

keyboard_inline = InlineKeyboardMarkup(inline_keyboard=buttons_inline)
