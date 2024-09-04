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

    @patch('tronenergy.tron_energy.requests.Session.post')
    def test_place_order(self, mock_get):
        # Arrange
        expected_response = {
            "errno": 0,
            "serial": "7297a8a2a9e39b86fc5bad0d2e9edda2",
            "amount": 3120000,
            "balance": 813900029257
        }
        mock_get.return_value.json.return_value = expected_response

        data = {
            "receive_address": "TR7NHnXw5423f8j766h899234567890",
            "energy_amount": 3120000,
            "period": "1H"
        }
    
        # Act
        response = self.tron_energy.place_order(**data)
    
        # Assert
        self.assertEqual(response, expected_response)

    @patch('tronenergy.tron_energy.requests.Session.post')
    def test_transfer_small_trx_amount(self, mock_get):
        # Arrange
        expected_response = {
            "errno": 0,
            "txid": "9df44479551ef93c9bbfeca3cb82ef1564199d2d492ad38f7f1d2e454f5efb0f",
            "balance": 813900029257
        }
        mock_get.return_value.json.return_value = expected_response

        data = {
            "receive_address": "TR7NHnXw5423f8j766h899234567890",
            "amount": 500_000 # 0.5 TRX
        }
    
        # Act
        response = self.tron_energy.transfer_small_trx_amount(**data)
    
        # Assert
        self.assertEqual(response, expected_response)

    @patch('tronenergy.tron_energy.requests.Session.post')
    def test_purchase_by_number_of_transfers(self, mock_get):
        # Arrange
        expected_response = {
            "errno": 0,
            "balance": 813900029257
        }
        mock_get.return_value.json.return_value = expected_response

        data = {
            "receive_address": "TR7NHnXw5423f8j766h899234567890",
            "times": 5 
        }
    
        # Act
        response = self.tron_energy.purchase_by_number_of_transfers(**data)
    
        # Assert
        self.assertEqual(response, expected_response)

    @patch('tronenergy.tron_energy.requests.Session.get')
    def test_list_purchases_by_number_of_transfers(self, mock_get):
        # Arrange
        expected_response = {
            "count": 2,
            "code": 0,
            "page": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 2,
                    "receive_address": "TEX5nLeFJ1dyazhJC3P9eYJs7hxgk7knJF",
                    "status": 1,
                    "last_step": 0,
                    "main_delegated": False,
                    "expired_time": None,
                    "create_time": "2023-08-23T11:09:27.986610+08:00",
                    "update_time": "2023-08-23T11:09:27.986660+08:00",
                    "last_step_display": "deledate",
                    "status_display": "enable",
                    "auto_type": 1,                     # 1-only energy，2-energy+bandwidth
                    "auto_type_display": "only energy",
                    "max_energy": 65000,
                    "period": 7,
                    "count_limit": 8                    # times
                },
            ]
        }
        mock_get.return_value.json.return_value = expected_response

        data = {
            "receive_address": "TR7NHnXw5423f8j766h899234567890",
        }
    
        # Act
        response = self.tron_energy.list_purchases_by_number_of_transfers(**data)
    
        # Assert
        self.assertEqual(response, expected_response)

    @patch('tronenergy.tron_energy.requests.Session.post')
    def test_create_smart_delegate(self, mock_get):
        # Arrange
        expected_response = {
            "errno": 0,
            "message": "1 smart delegate has been added",
            "balance": 813900029257

        }
        mock_get.return_value.json.return_value = expected_response

        data = {
            "receive_address": "TR7NHnXw5423f8j766h899234567890",
            "period": 1
        }
    
        # Act
        response = self.tron_energy.create_smart_delegate(**data)
    
        # Assert
        self.assertEqual(response, expected_response)

    @patch('tronenergy.tron_energy.requests.Session.get')
    def test_list_smart_delegate(self, mock_get):
        # Arrange
        expected_response = {
            "count": 1,
            "code": 0,
            "page": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 21,
                    "receive_address": "TNfdtE7p8pEfTTbfRb88gikf2tt5ENc86b",
                    "status": 1, # Is it valid?
                    "last_step": 1, 
                    "main_delegated": False, # Delegated status, valid during automatic renewal
                    "expired_time": None,
                    "create_time": "2023-10-09T11:13:12.288373+08:00",
                    "update_time": "2023-10-09T16:35:36.559760+08:00",
                    "last_step_display": "delegated",
                    "status_display": "on",
                    "auto_type": 1, # 1 is smart hosting, 2 is automatic renewal only
                    "auto_type_display": "smart hosting",
                    "next_delegate_time": None, # Valid during automatic renewal
                    "max_energy": 50000, # maintain energy
                    "period": 3, # Commission period
                },
            ]
        }

        mock_get.return_value.json.return_value = expected_response

        data = {
            "receive_address": "TR7NHnXw5423f8j766h899234567890",
        }
    
        # Act
        response = self.tron_energy.list_smart_delegate(**data)
    
        # Assert
        self.assertEqual(response, expected_response)

    @patch('tronenergy.tron_energy.requests.Session.post')
    def test_modify_smart_delegate(self, mock_get):
        # Arrange
        expected_response = {
            "errno": 0
        }
        mock_get.return_value.json.return_value = expected_response

        data = {
            "id": 21,
            "status": False,
        }
    
        # Act
        response = self.tron_energy.modify_smart_delegate(**data)
    
        # Assert
        self.assertEqual(response, expected_response)

    @patch('tronenergy.tron_energy.requests.Session.get')
    def test_get_order(self, mock_get):
        # Arrange
        expected_response = {
            "errno": 0,
            "receive_address": "TExWKszFWYTKZH8LYiovAPKzS3L9MLZ4kw",
            "order_no": "58b451473d290f92443eabf0322b9907",
            "energy_amount": 32000,
            "pay_amount": 0.0,
            "amount": 3800000,
            "details": [
                {
                    "delegate_hash": "e2e71df638a9e01492a50bebba072a39eb75f673e91d5374ccf517f44e113f3",
                    "delegate_time": "2023-10-09T10:21:07.840478Z",
                    "reclaim_hash": "f4672a9563947cf78e5534b4025451dfd75efa5481a67b20ee55b9be368c900",
                    "reclaim_time": "2023-10-12T10:21:07.840478Z",
                    "reclaim_time_real": "2023-10-09T10:26:12.617456Z",
                    "status": 30 # 20-in commission, 30-recycled
                }
            ],
            "create_time": "2023-06-15T21:42:13.200565+08:00",
            "api_name": "MY API",
            "period": 0,
            "status": 30, # 30 indicates that the commission was completely successful
            "refund_amount": 0
        }
        mock_get.return_value.json.return_value = expected_response

        data = {
            "order_no": "58b451473d290f92443eabf0322b9907"
        }
    
        # Act
        response = self.tron_energy.get_order(**data)
    
        # Assert
        self.assertEqual(response, expected_response)

    @patch('tronenergy.tron_energy.requests.Session.post')
    def test_recycle_order(self, mock_get):
        # Arrange
        expected_response = {
            "errno": 0,
            "message": "request accept"
        }
        mock_get.return_value.json.return_value = expected_response

        data = {
            "order_no": "58b451473d290f92443eabf0322b9907"
        }
    
        # Act
        response = self.tron_energy.recycle_order(**data)
    
        # Assert
        self.assertEqual(response, expected_response)

    @patch('tronenergy.tron_energy.requests.Session.get')
    def test_estimate_order(self, mock_get):
        # Arrange
        expected_response = {
            "period": "1H",
            "energy_amount": 32000,
            "price": 100,
            "total_price": 10192000,
            "addition": 600000
        }
        mock_get.return_value.json.return_value = expected_response

        data = {
            "energy_amount": 32000,
            "period": '1H',
            }
    
        # Act
        response = self.tron_energy.estimate_order(**data)
    
        # Assert
        self.assertEqual(response, expected_response)

    @patch('tronenergy.tron_energy.requests.Session.get')
    def test_get_api_usage_summary(self, mock_get):
        # Arrange
        expected_response = {
            "name": "MY API",
            "create_time": "2023-04-28 12:31:04",
            "total_count": 46,
            "total_sum_energy": 3696000,
            "total_sum_trx": 598165000,
            "today_count": 0,
            "today_sum_energy": 0,
            "today_sum_trx": 0,
            "yesterday_count": 1,
            "yesterday_sum_energy": 1300000,
            "yesterday_sum_trx": 197600000
        }
        mock_get.return_value.json.return_value = expected_response

        # Act
        response = self.tron_energy.get_api_usage_summary()
    
        # Assert
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()