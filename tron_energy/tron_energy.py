import os
import requests
import hmac
import hashlib
import json
from urllib.parse import urljoin
from time import time


TronAddress = str


class TronEnergy(object):
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
        self.sess = requests.session()
        self.sess.headers["API-KEY"] = api_key
        self.sess.headers["Content-Type"] = "application/json"

    def _get_timestamp(self):
        return str(int(time()))
    
    def _sign(self, message:str):
        return hmac.new(self._api_secret.encode(), message.encode(), hashlib.sha256).hexdigest()
    
    def _jsonify(self, data:dict):
        if data:
            return json.dumps(data, sort_keys=True, separators=(',', ':'))
        return ""
    
    def make_request(self, method:str, url:str, data:dict=None):
        timestamp = self._get_timestamp()
        headers = {"TIMESTAMP": timestamp}
        if method.upper() == "POST":
            json_data = self._jsonify(data)
            headers["SIGNATURE"] = self._sign(f'{timestamp}&{json_data}')
            response = self.sess.post(urljoin(self.base_url, url), data=json_data, headers=headers)
        else:
           response = self.sess.get(urljoin(self.base_url, url), params=data, headers=headers) 

        if response.status_code == 400:
            raise requests.exceptions.HTTPError(response.json())
        else:
            response.raise_for_status()
        return response.json()

    def verify_signature(self, signature:str, timestamp:str, data:dict):
       json_data = self._jsonify(data)
       expected_signature = self._sign(f"{timestamp}&{json_data}")
       return hmac.compare_digest(signature, expected_signature)
    
    def get_public_data(self):
        """
        Retrieves public data from the TronEnergy API.

        Returns:
        dict: A dictionary containing the public data retrieved from the API.
        """
        url = "/api/v1/frontend/index-data"
        return self.make_request("GET", url)
    
    def place_order(self, receive_address:TronAddress, energy_amount:int, period:str='1H', out_trade_no:str=None, callback_url:str=None):
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
        return self.make_request("POST", url, data)
    
    def transfer_small_trx_amount(self, amount:int, receive_address:TronAddress):
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
        return self.make_request("POST", url, data)
    
    def purchase_by_number_of_transfers(self, times:int, receive_address:TronAddress):
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
        return self.make_request("POST", url, data)
    
    def list_purchases_by_number_of_transfers(self, receive_address:TronAddress=None): # Note: We will have to do something about pagination here.
        """
        Parameters:
            receive_address (TronAddress): Query a specific address, if not filled in, return all.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        url = f"/api/v1/frontend/count-delegate-policy"
        data = {"receive_address": receive_address} if receive_address else None
        return self.make_request("GET", url, data)
    
    def create_smart_delegate(self, period:int, receive_address:TronAddress, max_energy:int=None):
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
        return self.make_request("POST", url, data)
    
    def list_smart_delegate(self, receive_address:TronAddress=None): # Note: We will have to do something about pagination here.
        """
        Parameters:
            receive_address (TronAddress): Query a specific address, if not filled in, return all.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        url = "/api/v1/frontend/auto-delegate-policy"
        data = {"receive_address": receive_address} if receive_address else None
        return self.make_request("GET", url, data)

    def modify_smart_delegate(self, id:int, status:bool):
        """
        Parameters:
            id (int): The ID of the smart delegate policy.
            status (bool): The new status of the smart delegate policy.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        url = f"/api/v1/frontend/auto-delegate-policy/{id}/change-status"
        data = {"status": int(status)} 
        return self.make_request("POST", url, data)

    def get_order(self, order_no:str):
        """
        Parameters:
            order_no (str): The order number returned when placing an order.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        url = "/api/v1/frontend/order/query"
        data = {"serial": order_no}
        return self.make_request("GET", url, data)
    
    def recycle_order(self, order_no:str):
        """
        Parameters:
            order_no (str): The order number returned when placing an order.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        url = "/api/v1/frontend/order/reclaim"
        data = {"serial": order_no}
        return self.make_request("POST", url, data)
    
    def estimate_order(self, energy_amount:int, period:str="1H"):
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
        return self.make_request("GET", url, data)
    
    def get_api_usage_summary(self):
        """
        Retrieves API usage summary.

        Returns:
            dict: A dictionary containing the API usage summary.
        """
        url = "/api/v1/frontend/userapi/summary"
        return self.make_request("GET", url)
        

 