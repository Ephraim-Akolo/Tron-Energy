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

    