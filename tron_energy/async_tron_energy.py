import os
import hashlib
import hmac
import json
from aiohttp import ClientSession, ClientResponseError, ClientResponse
from time import time
from urllib.parse import urljoin


TronAddress = str


class AsyncTronEnergy:
    base_url = 'https://itrx.io/'

    def __init__(self, api_key:str=None, api_secret:str=None):
        if not api_secret:
            api_secret = os.getenv('TRON_ENERGY_API_SECRET')
        if api_secret is None:
            raise ValueError("API secret is required")
        if not api_key:
            api_key = os.getenv('TRON_ENERGY_API_KEY')
        if api_key is None:
            raise ValueError("API key is required")
        
        self._api_secret = str(api_secret)
        self.sess = ClientSession(headers={
            'Content-Type': 'application/json',
            'API-KEY': api_key
        })

    async def close(self):
        await self.sess.close()

    def _sign(self, message:str):
        return hmac.new(self._api_secret.encode(), message.encode(), hashlib.sha256).hexdigest()

    def _jsonify(self, data:dict):
        if data:
            return json.dumps(data, sort_keys=True, separators=(',', ':'))
        return ""

    