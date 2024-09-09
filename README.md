
# Tron-Energy

Tron-Energy is a Python package that simplifies interaction with the [Tron energy](https://itrx.io/) lending RESTful API. It provides a clean and easy-to-use interface for placing energy orders, estimating costs, and managing your API usage on the Tron network. The package ensures secure communication with the API by handling signature creation and request authentication.

## Installation

To install the Tron-Energy package, run the command:

```bash
pip install tron_energy
```


Ensure you have Python 3.6 or higher installed.

## Usage

To use the Tron-Energy package, start by importing the necessary classes and creating an instance of the `TronEnergy` class.

Here’s an example of how you might use Tron-Energy to estimate the cost of an energy order and then place the order:

```python
from tron_energy import TronEnergy

# Initialize the TronEnergy client
client = TronEnergy(api_key='your-api-key', api_secret='your-api-secret')

# Retrieve public data
public_data = client.get_public_data()
print(public_data)

# Estimate the cost of an energy order
estimate = client.estimate_order(
    energy_amount=100_000,
    period='1H'
)
print(estimate)

# Place the energy order
order_response = client.place_order(
    receive_address="TR7NHnXw5423f8j766h899234567890",
    energy_amount=100_000,
    period='1H'
)
print(order_response)
```

## Asynchronous Usage

In addition to the synchronous interface, Tron-Energy provides an asynchronous version for applications requiring non-blocking I/O operations. The asynchronous class, AsyncTronEnergy, allows you to make API requests without blocking your event loop.

Here’s an example of how to use the asynchronous AsyncTronEnergy class:

```python
import asyncio
from tron_energy import AsyncTronEnergy

async def main():
    # Initialize the AsyncTronEnergy client
    client = AsyncTronEnergy(api_key='your-api-key', api_secret='your-api-secret')

    try:
        # Retrieve public data
        public_data = await client.get_public_data()
        print(public_data)

        # Estimate the cost of an energy order
        estimate = await client.estimate_order(
            energy_amount=100_000,
            period='1H'
        )
        print(estimate)

        # Place the energy order
        order_response = await client.place_order(
            receive_address="TR7NHnXw5423f8j766h899234567890",
            energy_amount=100_000,
            period='1H'
        )
        print(order_response)
    finally:
        # Close the session to clean up resources
        await client.close()

# Run the asynchronous main function
asyncio.run(main())

```

Or use the Python context manager:

```python
import asyncio
from tron_energy import AsyncTronEnergy

async def main():
    # Initialize the AsyncTronEnergy client
    async with AsyncTronEnergy(api_key='your-api-key', api_secret='your-api-secret') as client:
        # Retrieve public data
        public_data = await client.get_public_data()
        print(public_data)

        # Estimate the cost of an energy order
        estimate = await client.estimate_order(
            energy_amount=100_000,
            period='1H'
        )
        print(estimate)

        # Place the energy order
        order_response = await client.place_order(
            receive_address="TR7NHnXw5423f8j766h899234567890",
            energy_amount=100_000,
            period='1H'
        )
        print(order_response)

# Run the asynchronous main function
asyncio.run(main())

```

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
