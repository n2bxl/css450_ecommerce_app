# CSS/450 - Computer Science Capstone

A lightweight e-commerce application developed for CSS/450: Computer Science Capstone. The application demonstrates a minimum viable product (MVP) for a small independent or mobile coffee shop, allowing customers to browse beverages, customize supported options, manage a shopping cart, and submit an order.

## Features

- Browse available beverages by category.
- View beverage descriptions and prices.
- Customize supported beverage options, including size and milk type.
- Add configured beverages to a shopping cart.
- Increase, decrease, or remove items from the cart.
- Review subtotal, tax, and order total.
- Submit an order and receive an order confirmation.
- Prevent submission of an empty cart with guidance for returning to the menu.

## Requirements

Before installing the application, ensure the following are available:

- Python 3.12 or newer is recommended.
- Git is required when cloning the repository.

The application was developed and most recently verified using Python 3.14.6.

The required Python packages are listed in `requirements.txt` and include:

- Streamlit 1.64.0
- pytest 9.1.1

## Installation

### Windows

Clone the repository and enter the project directory:

```powershell
git clone https://github.com/n2bxl/css450_ecommerce_app.git
cd css450_ecommerce_app
```

Check the available Python version:

```powershell
py --version
```

If multiple versions of Python are installed, they can be displayed with:

```powershell
py -0p
```

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If multiple Python versions are installed, a specific recent version can be selected when creating the environment. For example:

```powershell
py -3.14 -m venv .venv
```

Install the required packages:

```powershell
python -m pip install -r requirements.txt
```

### macOS

Clone the repository and enter the project directory:

```bash
git clone https://github.com/n2bxl/css450_ecommerce_app.git
cd css450_ecommerce_app
```

Check the installed Python version:

```bash
python3 --version
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

### Linux

Clone the repository and enter the project directory:

```bash
git clone https://github.com/n2bxl/css450_ecommerce_app.git
cd css450_ecommerce_app
```

Check the installed Python version:

```bash
python3 --version
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

> Some Linux distributions package Python virtual environment support separately. If `python3 -m venv` is unavailable, install the appropriate `venv` package for the installed Python version before continuing.

## Running the Application

With the virtual environment activated, start the Streamlit application from the project directory:

```bash
python -m streamlit run app.py
```

Streamlit will display the local application address in the terminal and may open the application automatically in the default web browser.

To stop the application, press `Ctrl+C` in the terminal.

## Running the Tests

With the virtual environment activated, run the automated test suite from the project directory:

```bash
pytest
```

The Week Four handoff build at commit `db11284` contains 29 automated tests covering the cart, cart interface, beverage customization, menu repository, menu service, and order service.

## Project Structure

```text
css450_ecommerce_app/
├── app.py
├── data/
├── models/
├── repositories/
├── services/
├── tests/
├── pytest.ini
├── requirements.txt
└── README.md
```

- `app.py` contains the Streamlit user interface and application flow.
- `data/` contains application data used by the MVP.
- `models/` defines application data models.
- `repositories/` handles access to stored application data.
- `services/` contains application and business logic.
- `tests/` contains the automated pytest suite.

## Known Limitations

This application is an MVP developed within the scope of the CSS/450 capstone project.

Order confirmation is implemented, but completed orders are not durably stored for later retrieval by the coffee shop. Persistent order storage and a shop-side order retrieval workflow are planned future enhancements.

The application is designed as a demonstration and has not been developed or load tested for production-scale traffic.

## Course Information

This project was developed for CSS/450: Computer Science Capstone at the University of Phoenix. It demonstrates the design, development, testing, and evaluation of an e-commerce minimum viable product.