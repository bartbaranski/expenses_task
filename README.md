Expenses Task

This repository implements a solution for the Python coding challenge, including:
    Task 1: A CLI tool (expenses.py) to aggregate company expenses by department, year, quarter, or month.
    Task 2: A stateless REST API service (app.py) built with FastAPI.
    Task 3: A comprehensive test suite using pytest and FastAPI’s TestClient to validate API behaviors.
    Database Schema: A schema definition (database_schema.sql).

Project Structure
    expenses_task/
    ├── expenses.py            # CLI application
    ├── app.py                 # FastAPI REST service
    ├── database_schema.sql    # PostgreSQL for table schema
    ├── erd_db.png             # Database schema
    ├── requirements.txt       # Python dependencies
    ├── README.md              # Project documentation (this file)
    └── test_api.py            # Tests for REST API

Task 1: CLI Tool (expenses.py)
    Reads CSV data from standard input and prints aggregated expense totals.

    Usage
    cat Expenses.csv | python3 expenses.py <department>
    cat Expenses.csv | python3 expenses.py <department> <year>
    cat Expenses.csv | python3 expenses.py <department> <year> <quarter>
    cat Expenses.csv | python3 expenses.py <department> <year> <month_name>
    
    <department>: exact department name
    <year>: four‑digit year (e.g. 2020)
    <quarter>: integer 1–4 (only quarter filtering)
    <month_name>: full or abbreviated month name (e.g. January or Jan)

    e.g.: cat Expenses.csv | python3 expenses.py "Human Resources" 2020

    Error conditions include missing CSV header, invalid quarter, or unrecognized month name.

Task 2: REST API (app.py)
    An HTTP POST endpoint at /aggregate accepts CSV data in the request body and query parameters for aggregation.

    Running the server
        python3 -m uvicorn app:app --reload

    Endpoint
        POST /aggregate?department=<dept>&[year=<year>]&[quarter=<1-4>]|[month=<month_name>]
        Content-Type: text/csv
        Body: raw CSV data

    Example
        curl.exe -X POST "http://127.0.0.1:8000/aggregate?department=Sales&year=2020&quarter=1"   -H "Content-Type: text/csv"   --data-binary "@Expenses.csv"

    Response JSON:
        { "total_expenses": 12345.67, "currency": "USD" }

    Error responses use HTTP 400 with detailed messages for missing body, empty CSV, invalid params, etc.

    Database Schema (database_schema.sql)

Defines a schema with:
    department
    expense_type
    date_dim
    expense_fact

    It was tested in PostgreSQL.


Tests (tests/)
    Run all tests with:
        pytest

    The suite covers successful and error cases for the REST API.
