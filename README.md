# Store Management System

A command-line store application built with Python and object-oriented programming (OOP). This project simulates a small retail store with different product types, inventory management, promotions, and order processing.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![OOP](https://img.shields.io/badge/Concept-OOP-orange)
![Tests](https://img.shields.io/badge/Tests-pytest-green)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- Display all active products in the store
- Show the total quantity of stocked products
- Create and process customer orders
- Validate user input and purchase quantities
- Track product inventory and sold-out products
- Support non-stocked products
- Support products with a maximum purchase quantity
- Apply product promotions:
  - Percentage discounts
  - Second item at half price
  - Buy two, get one free
- Display active promotions when products are listed
- Validate complete orders before modifying inventory
- Automated unit tests with pytest

## Project Structure

```text
.
├── main.py
├── products.py
├── promotions.py
├── store.py
├── tests/
│   ├── test_product.py
│   ├── test_promotions.py
│   └── test_store.py
├── requirements.txt
├── README.md
└── LICENSE
```

### Main Components

**`products.py`**

Contains the product classes:

- `Product` — standard stocked product
- `NonStockedProduct` — product without physical inventory
- `LimitedProduct` — product with a maximum purchase quantity per order

**`promotions.py`**

Contains the promotion classes:

- `Promotion` — abstract base class
- `PercentDiscount` — percentage-based discount
- `SecondHalfPrice` — every second item is half price
- `ThirdOneFree` — every third item is free

**`store.py`**

Contains the `Store` class, which manages products and processes orders.

**`main.py`**

Contains the command-line interface, user input handling, store setup, and application entry point.

**`tests/`**

Contains the automated pytest test suite for products, promotions, and store functionality.

## Running the Application

Make sure Python 3 is installed, then run:

```bash
python main.py
```

Follow the instructions displayed in the command line to browse products and create orders.

## Running the Tests

The project uses `pytest` for automated testing.

Install the project dependencies with:

```bash
pip install -r requirements.txt
```

Run all tests with:

```bash
pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.