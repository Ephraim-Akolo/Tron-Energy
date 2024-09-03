import unittest
from tronenergy import TronEnergy

class TestTronEnergySignatureVerification(unittest.TestCase):
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

        result = self.tron_energy.verify_signature(signature, timestamp, data)

        # Assert
        self.assertTrue(result)

    

if __name__ == '__main__':
    unittest.main()