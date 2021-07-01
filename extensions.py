import requests
import json
from config import keys

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def conver(in_values, out_values, amount):
        if in_values == out_values:
            raise APIException(f"Валюты одинаковые. невозможно перевести {in_values} в {out_values}")
        try:
            amount = int(amount)
        except ValueError:
            raise APIException("Колличество не понятно")
        try:
            in_values_ticker = (keys[in_values])
        except KeyError:
            raise APIException(f"Не удалось распознать валюту {in_values}")
        try:
            out_values_ticker = (keys[out_values])
        except KeyError:
            raise APIException(f"Не удалось распознать валюту {out_values}")
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={in_values_ticker}&tsyms={out_values_ticker}')
        text_out = json.loads(r.content)[keys[out_values]]
        return text_out*amount