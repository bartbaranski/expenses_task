import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)
CSV = """Department;Expense Type;Year;Jan;Feb;Mar;Apr;May;Jun;Jul;Aug;Sep;Oct;Nov;Dec
Sales;Software;2020;$1;$2;$3;$4;$5;$6;$7;$8;$9;$10;$11;$12
"""

#successful

def test_api_department_only():
    response = client.post("/aggregate?department=Sales", data=CSV, headers={"Content-Type":"text/csv"})
    assert response.status_code == 200
    assert response.json()["total_expenses"] == pytest.approx(78.0)

def test_api_year_and_quarter():
    response = client.post(
        "/aggregate?department=Sales&year=2020&quarter=1",
        data=CSV,
        headers={"Content-Type":"text/csv"}
    )
    assert response.status_code == 200
    assert response.json()["total_expenses"] == pytest.approx(6.0)

def test_api_month_name():
    response = client.post(
        "/aggregate?department=Sales&year=2020&month=January",
        data=CSV,
        headers={"Content-Type":"text/csv"}
    )
    assert response.status_code == 200
    assert response.json()["total_expenses"] == pytest.approx(1.0)

#errors

def test_api_missing_body():
    response = client.post("/aggregate?department=Sales")
    assert response.status_code == 400
    assert "Missing CSV data" in response.json()["detail"]

def test_api_empty_csv():
    response = client.post(
        "/aggregate?department=Sales",
        data="",
        headers={"Content-Type":"text/csv"}
    )
    assert response.status_code == 400
    assert "CSV contains no data" in response.json()["detail"]

def test_api_both_quarter_and_month():
    response = client.post(
        "/aggregate?department=Sales&quarter=1&month=January",
        data=CSV,
        headers={"Content-Type":"text/csv"}
    )
    assert response.status_code == 400
    assert "Provide either quarter or month" in response.json()["detail"]

def test_api_invalid_quarter():
    response = client.post(
        "/aggregate?department=Sales&quarter=5",
        data=CSV,
        headers={"Content-Type":"text/csv"}
    )
    assert response.status_code == 400
    assert "Invalid quarter" in response.json()["detail"]

def test_api_numeric_month():
    response = client.post(
        "/aggregate?department=Sales&month=5",
        data=CSV,
        headers={"Content-Type":"text/csv"}
    )
    assert response.status_code == 400
    assert "Month must be a valid name" in response.json()["detail"]

def test_api_invalid_month_name():
    response = client.post(
        "/aggregate?department=Sales&month=Foo",
        data=CSV,
        headers={"Content-Type":"text/csv"}
    )
    assert response.status_code == 400
    assert "Invalid month name" in response.json()["detail"]

@pytest.fixture
def csv_missing_header():
    return """Dept;Jan
Sales;100
"""

def test_api_missing_department_header(csv_missing_header):
    response = client.post(
        "/aggregate?department=Sales",
        data=csv_missing_header,
        headers={"Content-Type":"text/csv"}
    )
    assert response.status_code == 400
    assert "missing 'Department'" in response.json()["detail"]