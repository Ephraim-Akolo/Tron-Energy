import requests
from time import time


class TronEnergy(object):
    base_url = 'https://itrx.io/'


    def get_timestamp(self):
        return str(int(time()))

    
