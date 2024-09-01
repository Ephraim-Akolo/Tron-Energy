import requests
import hmac
import hashlib
import json
from urllib.parse import urljoin
from time import time


TronAddress = str


class TronEnergy(object):
    base_url = 'https://itrx.io/'

    def __init__(self, api_key:str, api_secret:str):
        self._api_secret = api_secret
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
    
    def make_request(self, method, url, data=None):
        timestamp = self._get_timestamp()
        headers = {"TIMESTAMP": timestamp}
        if method.upper() == "POST":
            json_data = self._jsonify(data)
            headers["SIGNATURE"] = self._sign(f'{timestamp}&{json_data}')
            response = self.sess.post(urljoin(self.base_url, url), data=json_data, headers=headers)
        else:
           response = self.sess.get(urljoin(self.base_url, url), headers=headers) 

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

        This function sends a GET request to the '/api/v1/frontend/index-data' endpoint
        to retrieve public data. The request includes the necessary headers for authentication.

        Returns:
        dict: A dictionary containing the public data retrieved from the API.
        """
        url = "/api/v1/frontend/index-data"
        return self.make_request("GET", url)
    
    

    
