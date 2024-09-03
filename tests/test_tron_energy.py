import unittest
from unittest.mock import patch, Mock
from tronenergy import TronEnergy

class TestTronEnergyMethods(unittest.TestCase):
    def setUp(self):
        self.tron_energy = TronEnergy(api_key='your_api_key', api_secret='your_api_secret')

    def test_verify_signature(self):
        # Arrange
        timestamp = self.tron_energy._get_timestamp()
        data = {
            'energy_amount': 100,
            'period': '1H',
        }
        signature = self.tron_energy._sign(f"{timestamp}&{self.tron_energy._jsonify(data)}")

        # Act
        result = self.tron_energy.verify_signature(signature, timestamp, data)

        # Assert
        self.assertTrue(result)

    @patch('tronenergy.tron_energy.requests.Session.get')
    def test_get_public_data(self, mock_get):
        # Arrange
        expected_response = {
            "platform_avail_energy": 603249,
            "platform_max_energy": 329009,
            "minimum_order_energy": 32000,
            "maximum_order_energy": 100000000,
            "small_amount": 50000,
            "small_addition": 0.6,
            "usdt_energy_need_old": 32000,
            "usdt_energy_need_new": 65000,
            "tiered_pricing": [{"period": 0, "price": 100}, {"period": 1, "price": 200}, {"period": 3, "price": 152}, {"period ": 30, "price": 124}],
            "balance": 813892429257
        }
        mock_get.return_value.json.return_value = expected_response
    
        # Act
        response = self.tron_energy.get_public_data()
    
        # Assert
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()