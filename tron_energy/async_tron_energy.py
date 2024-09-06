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

    def _get_timestamp(self):
        return str(int(time()))
    
    async def _handle_response(self, response:ClientResponse):
        try:
            json_response = await response.json()
        except json.JSONDecodeError as e:
            response.raise_for_status()
            raise Exception(f"Failed to decode JSON: {e}")
        
        if response.status >= 300 or response.status < 200:
            raise ClientResponseError(
                request_info=response.request_info,
                history=response.history,
                status=response.status,
                message=json_response,
                headers=response.headers
            )
        
        return json_response
    
    async def make_request(self, method: str, url: str, data: dict = None):
        timestamp = self._get_timestamp()
        headers = {"TIMESTAMP": timestamp}
        
        if method.upper() == "POST":
            json_data = self._jsonify(data)
            headers["SIGNATURE"] = self._sign(f'{timestamp}&{json_data}')
            async with self.sess.post(urljoin(self.base_url, url), data=json_data, headers=headers) as response:
                return await self._handle_response(response)
        else:
            async with self.sess.get(urljoin(self.base_url, url), params=data, headers=headers) as response:
                return await self._handle_response(response)

    