import requests
import hmac
import hashlib
import json
from time import time


class TronEnergy(object):
    base_url = 'https://itrx.io/'

    def __init__(self, api_key, api_secret):
        self._api_key = api_key
        self._api_secret = api_secret

    def get_timestamp(self):
        return str(int(time()))
    
    def sign(self, message:str):
        return hmac.new(self._api_secret.encode(), message.encode(), hashlib.sha256).hexdigest()
    
    def jsonify(self, data:dict):
        return json.dumps(data, sort_keys=True, separators=(',', ':'))

    
