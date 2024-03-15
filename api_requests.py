"""Модуль запросов к API WB."""
import http
import json

import requests
from requests.exceptions import HTTPError, RequestException

from constants import URL_API_WB


def get_api_answer(article):
    """
    Функция выполняет запрос к API WB,
    выбирает нужные данные из запроса.
    """
    try:
        api_answer = requests.get(URL_API_WB.format(article))
        if api_answer.status_code != http.HTTPStatus.OK:
            raise HTTPError(f"API WB вернул: {api_answer.status_code}")
        answer = api_answer.json()
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Ошибка декодирования JSON: {e}")
    except RequestException as e:
        raise RuntimeError(f"API сервиса WB недоступен: {e}")
    products = answer.get("data").get("products")
    if len(products) != 0:
        name = products[0].get("name")
        id = products[0].get("id")
        price = products[0].get("salePriceU")
        rating = products[0].get("rating")
        amount_all = 0
        for i in products[0].get("sizes")[0].get("stocks"):
            amount_all += int(i.get("qty"))
        return (name, id, price, rating, amount_all)
    elif len(products) == 0:
        raise KeyError("API вернул пустой список 'products'")
