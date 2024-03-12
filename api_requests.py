import requests
from pprint import pprint

from constants import URL_API_WB


def get_api_answer(article):
    api_answer = requests.get(URL_API_WB.format(article))
    print(type(api_answer))
    pprint(api_answer)
    # pprint(api_answer.get("data").get("products")[0].get("priceU"))


get_api_answer("19976250")
