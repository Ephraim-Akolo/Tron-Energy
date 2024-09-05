
# Tron-Energy

Tron-Energy is a Python package designed to simplify interaction with the [Tron energy](https://itrx.io/) lending RESTful API. It provides a clean and easy-to-use interface for placing energy orders, estimating costs, and managing your API usage on the Tron network. The package ensures secure communication with the API by handling signature creation and request authentication.

## Features

- Retrieve public data from the TronEnergy API.
- Place energy orders with customizable parameters.
- Estimate the cost of energy orders before placing them.
- Manage and monitor API usage effectively.
- Secure API requests with HMAC-based signature verification.

## Installation

To install the Tron-Energy package, run the command:

```bash
pip install tron_energy
```


Ensure you have Python 3.6 or higher installed.

## Usage

To use the Tron-Energy package, start by importing the necessary classes and creating an instance of the `TronEnergy` class:

```python
from tron_energy import TronEnergy

# Create an instance of TronEnergy
tron_energy = TronEnergy(api_key='your-api-key', api_secret='your-api-secret')

# Retrieve public data
public_data = tron_energy.get_public_data()
print(public_data)

# Place an energy order
order_response = tron_energy.place_order(
    receive_address="TR7NHnXw5423f8j766h899234567890",
    energy_amount=100_000
)
print(order_response)
```

### Example

Here’s an example of how you might use Tron-Energy to estimate the cost of an energy order and then place the order:

```python
from tron_energy import TronEnergy

# Initialize the TronEnergy client
tron_energy = TronEnergy(api_key='your-api-key', api_secret='your-api-secret')

# Estimate the cost of an energy order
estimate = tron_energy.estimate_order(
    energy_amount=100_000,
    period='1H'
)
print(estimate)

# Place the energy order
order_response = tron_energy.place_order(
    receive_address="TR7NHnXw5423f8j766h899234567890",
    energy_amount=100_000,
    period='1H'
)
print(order_response)
```

## API Reference

### `TronEnergy`

- **`__init__(self, api_key: str, api_secret: str)`**
  - Initializes the `TronEnergy` object with the given API key and secret.
  
- **`get_public_data(self) -> dict`**
  - Retrieves public data from the TronEnergy API.
  
- **`place_order(self, receive_address: TronAddress, energy_amount: int, period: str = '1H', out_trade_no: str = None, callback_url: str = None) -> dict`**
  - Places an energy order on the TronEnergy API.

- **`make_request(self, method: str, url: str, data: dict = None) -> dict`**
  - Makes a request to the TronEnergy API.

- **`verify_signature(self, signature: str, timestamp: str, data: dict) -> bool`**
  - Verifies the authenticity of a signature.


## Testing

The package includes unit tests to ensure that all functionalities work as expected. You can run the tests using the following command:

1. Clone the repository:

   ```bash
   git clone https://github.com/Ephraim-Akolo/Tron-Energy
   ```

2. Navigate to the project directory:

   ```bash
   cd TRON-ENERGY
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the following command to test
    ```bash
    python -m unittest
    ```

The tests cover various functionalities, including placing orders, estimating orders, and recycling orders. Mocking is used to simulate API responses.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

This package was inspired by and partially based on the examples and guidelines in the [Tron Energy API Documentation](https://develop.itrx.io/100-before.html). We appreciate the comprehensive resources provided by the Tron Energy team.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

---

Feel free to reach out with any questions or feedback!
