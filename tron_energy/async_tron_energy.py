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

    def verify_signature(self, signature, timestamp, data):
        computed_signature = self._sign(f"{timestamp}&{self._jsonify(data)}")
        return hmac.compare_digest(computed_signature, signature)

    async def get_public_data(self):
        """
        Retrieves public data from the TronEnergy API.

        Returns:
        dict: A dictionary containing the public data retrieved from the API.
        """
        url = "/api/v1/frontend/index-data"
        return await self.make_request("GET", url)

    async def place_order(self, receive_address:TronAddress, energy_amount:int, period:str='1H', out_trade_no:str=None, callback_url:str=None):
        """
        Places an energy order on the TronEnergy API.

        Parameters:
            receive_address (TronAddress): The Tron address where the energy will be received. The address needs to be activated, otherwise the order will fail.
            energy_amount (int): The amount of energy to be ordered.
            period (str, optional): The period for which the energy is to be ordered. Defaults to '1H'.
            out_trade_no (str, optional): The unique identifier for the order.
            callback_url (str, optional): The URL to which the API will send a callback when the order is fulfilled.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        url = "/api/v1/frontend/order"
        data = {
            "receive_address": receive_address,
            "energy_amount": energy_amount,
            "period": period,
        }
        if out_trade_no:
            data["out_trade_no"] = out_trade_no
        if callback_url:
            data["callback_url"] = callback_url
        return await self.make_request("POST", url, data)

    async def transfer_small_trx_amount(self, amount:int, receive_address:TronAddress):
        """
        Transfers small Tron amount to a specified address.

        Parameters:
            amount (int): The amount of Tron in Sun to be transferred between 100000 - 10000000. That is, between 0.1-10 TRX
            receive_address (TronAddress): The Tron address to which the Tron will be transferred.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        url = "/api/v1/frontend/order/transfer"
        data = {
            "amount": amount,
            "receive_address": receive_address,
        }
        return await self.make_request("POST", url, data)

    async def purchase_by_number_of_transfers(self, times:int, receive_address:TronAddress):
        """
        Parameters:
            times (int): Number of purchases, 5-1000 times
            receive_address (TronAddress): The Tron address to which the resources will be transferred.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        url = "/api/v1/frontend/count-delegate-policy"
        data = {
            "times": times,
            "receive_address": receive_address,
        }
        return await self.make_request("POST", url, data)

    async def list_purchases_by_number_of_transfers(self, receive_address:TronAddress=None): # Note: We will have to do something about pagination here.
        """
        Parameters:
            receive_address (TronAddress): Query a specific address, if not filled in, return all.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        url = f"/api/v1/frontend/count-delegate-policy"
        data = {"receive_address": receive_address} if receive_address else None
        return await self.make_request("GET", url, data)

    async def create_smart_delegate(self, period:int, receive_address:TronAddress, max_energy:int=None):
        """
        Parameters:
            period (int): The commission period, 1-30.
            receive_address (TronAddress): The Tron address to which the energy will be received.The address needs to be activated, otherwise the order will fail.
            max_energy (int, optional): The Amount to keep available.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        url = "/api/v1/frontend/auto-delegate-policy"
        data = {
            "period": period,
            "receive_address": receive_address,
        }
        if max_energy:
            data["max_energy"] = max_energy
        return await self.make_request("POST", url, data)

    async def list_smart_delegate(self, receive_address:TronAddress=None): # Note: We will have to do something about pagination here.
        """
        Parameters:
            receive_address (TronAddress): Query a specific address, if not filled in, return all.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        url = "/api/v1/frontend/auto-delegate-policy"
        data = {"receive_address": receive_address} if receive_address else None
        return await self.make_request("GET", url, data)

    async def modify_smart_delegate(self, id:int, status:bool):
        """
        Parameters:
            id (int): The ID of the smart delegate policy.
            status (bool): The new status of the smart delegate policy.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        url = f"/api/v1/frontend/auto-delegate-policy/{id}/change-status"
        data = {"status": int(status)} 
        return await self.make_request("POST", url, data)

    async def get_order(self, order_no:str):
        """
        Parameters:
            order_no (str): The order number returned when placing an order.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        url = "/api/v1/frontend/order/query"
        data = {"serial": order_no}
        return await self.make_request("GET", url, data)

    async def recycle_order(self, order_no:str):
        """
        Parameters:
            order_no (str): The order number returned when placing an order.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        url = "/api/v1/frontend/order/reclaim"
        data = {"serial": order_no}
        return await self.make_request("POST", url, data)

    async def estimate_order(self, energy_amount:int, period:str="1H"):
        """
        Estimates the price of an energy order.

        Parameters:
            energy_amount (int): The amount of energy to be ordered.
            period (str, optional): The period for which the energy is to be ordered. Defaults to '1H'.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        url = "/api/v1/frontend/order/price"
        data = {
            "energy_amount": energy_amount,
            "period": period,
        }
        return await self.make_request("GET", url, data)

    async def get_api_usage_summary(self):
        """
        Retrieves API usage summary.

        Returns:
            dict: A dictionary containing the API usage summary.
        """
        url = "/api/v1/frontend/userapi/summary"
        return await self.make_request("GET", url)
    
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.close()


