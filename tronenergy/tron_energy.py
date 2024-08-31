import requests
from time import time


class TronEnergy(object):
    base_url = 'https://itrx.io/'

    def __init__(self, api_key, api_secret):
        self._api_key = api_key
        self._api_secret = api_secret

    def get_timestamp(self):
        return str(int(time()))

    
