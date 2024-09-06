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

    