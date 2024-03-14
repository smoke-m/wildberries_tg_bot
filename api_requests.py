"""Модуль запросов к API WB."""

import requests

from constants import URL_API_WB


def get_api_answer(article):
    """
    Функция выполняет запрос к API WB,
    выбирает нужные данные из запроса.
    """
    answ = requests.get(URL_API_WB.format(article)).json()
    name = answ.get("data").get("products")[0].get("name")
    id = answ.get("data").get("products")[0].get("id")
    price = answ.get("data").get("products")[0].get("salePriceU")
    rating = answ.get("data").get("products")[0].get("rating")
    amount_all = 0
    for i in answ.get("data").get("products")[0].get("sizes")[0].get("stocks"):
        amount_all += int(i.get("qty"))
    return (name, id, price, rating, amount_all)
