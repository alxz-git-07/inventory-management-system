<!-- # Flask Inventory Management System

## Overview

This is a simple Flask-based inventory management API. It stores inventory items in memory and can optionally fetch product details from OpenFoodFacts when a barcode is provided.

You can use Postman to test the API endpoints.

## Requirements

- Python 3.10+
- pip
- Flask
- requests

## Setup

1. Open a terminal in the project folder:

   ```bash
   git clone <url-repo>
   cd flask-inventory-management-system
   pipenv install
   pipenv shell
```

## Running the App
Start the Flask Server with: -->

# Flask Inventory Management System

## Overview
Simple Flask REST API to manage an in-memory inventory. When a barcode is provided, the app will attempt to fetch product name and category from OpenFoodFacts.

Test the API with Postman.

## Requirements
- Python 3.10+
- pip
- virtualenv (or use built-in venv)
- Flask
- requests

## Setup

1. Install dependencies:
   ```bash
   git clone <url-repo>
   cd flask-inventory-management-system
   pipenv install
   pipenv shell

   ```

## Running the app
Start the Flask server:
```bash
python app.py
```

## API Endpoints
Base URL: http://127.0.0.1:5000

- Create item
  - POST /inventory
  - Body (application/json):
    ```json
    {
      "barcode": "737628064502",
      "quantity": 10,
      "price": 19.99
    }
    ```
  - If name/category are omitted the app will try to fetch them from OpenFoodFacts using the barcode.

- List items
  - GET /inventory

- Get item
  - GET /inventory/<barcode>

- Update item
  - PUT /inventory/<barcode>
  - Body (application/json): any of name, category, quantity, price

- Delete item
  - DELETE /inventory/<barcode>
  - Returns 204 on success (no body).

## Example Postman usage
1. Start the server.
2. Open Postman → New Request.
3. Set method and URL (e.g., POST http://127.0.0.1:5000/inventory).
4. For POST/PUT set Body → raw → JSON and paste the example JSON.
5. Send and inspect response.




