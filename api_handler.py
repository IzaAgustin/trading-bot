# api_handler.py
import requests
from config import APIS, API_KEYS

class APIHandler:
    def __init__(self):
        self.session = requests.Session()

    def get_from_coingecko(self, endpoint, params={}):
        url = f"{APIS['coingecko']}/{endpoint}"
        try:
            response = self.session.get(url, params=params)
            return response.json()
        except Exception as e:
            print("[CoinGecko Error]", e)
            return None

    def get_from_coinmarketcap(self, endpoint, params={}):
        url = f"{APIS['coinmarketcap']}/{endpoint}"
        headers = {"X-CMC_PRO_API_KEY": API_KEYS['coinmarketcap']}
        try:
            response = self.session.get(url, headers=headers, params=params)
            return response.json()
        except Exception as e:
            print("[CoinMarketCap Error]", e)
            return None

    def get_from_lunarcrush(self, endpoint, params={}):
        url = f"{APIS['lunarcrush']}/{endpoint}"
        params['key'] = API_KEYS['lunarcrush']
        try:
            response = self.session.get(url, params=params)
            return response.json()
        except Exception as e:
            print("[LunarCrush Error]", e)
            return None

    def get_fear_and_greed_index(self):
        try:
            response = self.session.get(APIS['alternative'])
            return response.json()
        except Exception as e:
            print("[Alternative.me Error]", e)
            return None
