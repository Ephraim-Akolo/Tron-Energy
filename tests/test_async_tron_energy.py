import unittest
from unittest.mock import AsyncMock, patch
from tron_energy import AsyncTronEnergy

class TestTronEnergyMethods(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.tron_energy = AsyncTronEnergy(api_key='your_api_key', api_secret='your_api_secret')

    async def asyncTearDown(self):
        await self.tron_energy.close()

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

    @patch('tron_energy.async_tron_energy.ClientSession.get')
    async def test_get_public_data(self, mock_get):
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

        # Mock the response object
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=expected_response)

        # Mock the context manager
        mock_get.return_value.__aenter__.return_value = mock_response
        mock_get.return_value.__aexit__.return_value = AsyncMock()

        # Act
        response = await self.tron_energy.get_public_data()

        # Assert
        self.assertEqual(response, expected_response)

    @patch('tron_energy.async_tron_energy.ClientSession.post')
    async def test_place_order(self, mock_get):
        # Arrange
        expected_response = {
            "errno": 0,
            "serial": "7297a8a2a9e39b86fc5bad0d2e9edda2",
            "amount": 3120000,
            "balance": 813900029257
        }
        # Mock the response object
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=expected_response)

        # Mock the context manager
        mock_get.return_value.__aenter__.return_value = mock_response
        mock_get.return_value.__aexit__.return_value = AsyncMock()

        data = {
            "receive_address": "TR7NHnXw5423f8j766h899234567890",
            "energy_amount": 3120000,
            "period": "1H"
        }
    
        # Act
        response = await self.tron_energy.place_order(**data)
    
        # Assert
        self.assertEqual(response, expected_response)

    @patch('tron_energy.async_tron_energy.ClientSession.post')
    async def test_transfer_small_trx_amount(self, mock_get):
        # Arrange
        expected_response = {
            "errno": 0,
            "txid": "9df44479551ef93c9bbfeca3cb82ef1564199d2d492ad38f7f1d2e454f5efb0f",
            "balance": 813900029257
        }
        
        # Mock the response object
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=expected_response)

        # Mock the context manager
        mock_get.return_value.__aenter__.return_value = mock_response
        mock_get.return_value.__aexit__.return_value = AsyncMock()

        data = {
            "receive_address": "TR7NHnXw5423f8j766h899234567890",
            "amount": 500_000 # 0.5 TRX
        }
    
        # Act
        response = await self.tron_energy.transfer_small_trx_amount(**data)
    
        # Assert
        self.assertEqual(response, expected_response)

    @patch('tron_energy.async_tron_energy.ClientSession.post')
    async def test_purchase_by_number_of_transfers(self, mock_get):
        # Arrange
        expected_response = {
            "errno": 0,
            "balance": 813900029257
        }
        
        # Mock the response object
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=expected_response)

        # Mock the context manager
        mock_get.return_value.__aenter__.return_value = mock_response
        mock_get.return_value.__aexit__.return_value = AsyncMock()

        data = {
            "receive_address": "TR7NHnXw5423f8j766h899234567890",
            "times": 5 
        }
    
        # Act
        response = await self.tron_energy.purchase_by_number_of_transfers(**data)
    
        # Assert
        self.assertEqual(response, expected_response)

    @patch('tron_energy.async_tron_energy.ClientSession.get')
    async def test_list_purchases_by_number_of_transfers(self, mock_get):
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
        
        # Mock the response object
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=expected_response)

        # Mock the context manager
        mock_get.return_value.__aenter__.return_value = mock_response
        mock_get.return_value.__aexit__.return_value = AsyncMock()

        data = {
            "receive_address": "TR7NHnXw5423f8j766h899234567890",
        }
    
        # Act
        response = await self.tron_energy.list_purchases_by_number_of_transfers(**data)
    
        # Assert
        self.assertEqual(response, expected_response)

    @patch('tron_energy.async_tron_energy.ClientSession.post')
    async def test_create_smart_delegate(self, mock_get):
        # Arrange
        expected_response = {
            "errno": 0,
            "message": "1 smart delegate has been added",
            "balance": 813900029257

        }
        
        # Mock the response object
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=expected_response)

        # Mock the context manager
        mock_get.return_value.__aenter__.return_value = mock_response
        mock_get.return_value.__aexit__.return_value = AsyncMock()

        data = {
            "receive_address": "TR7NHnXw5423f8j766h899234567890",
            "period": 1
        }
    
        # Act
        response = await self.tron_energy.create_smart_delegate(**data)
    
        # Assert
        self.assertEqual(response, expected_response)

    