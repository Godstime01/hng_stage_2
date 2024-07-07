import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_register_user_successfully(client):
    response = client.post(
        "/auth/register/",
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
        },
        format="json",
    )

    assert response.status_code == 201
    data = response.json()
    # print(data)
    assert "user" in data.get('data')
    assert data['data']["user"]["first_name"] == "John"
    assert "accessToken" in data.get('data')


@pytest.mark.django_db
def test_login_user_successfully(client):
    # First, register the user
    client.post(
        "/auth/register/",
        {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "password123",
        },
        format="json",
    )

    # Then, attempt to login
    response = client.post(
        "/auth/login/",
        {"email": "jane.doe@example.com", "password": "password123"},
        format="json",
    )

    assert response.status_code == 200
    data = response.json()
    assert "user" in data.get('data')
    assert "accessToken" in data.get('data')


@pytest.mark.django_db
def test_register_missing_fields(client):
    response = client.post(
        "/auth/register/",
        {"first_name": "John", "last_name": "Doe", "password": "password123"},
        format="json",
    )

    assert response.status_code == 422
    data = response.json()
    assert "errors" in data
    assert "email" in data["errors"][0]


@pytest.mark.django_db
def test_register_duplicate_email(client):
    client.post(
        "/auth/register/",
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "duplicate@example.com",
            "password": "password123",
        },
        format="json",
    )

    response = client.post(
        "/auth/register/",
        {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "duplicate@example.com",
            "password": "password123",
        },
        format="json",
    )

    assert response.status_code == 422
    data = response.json()
    assert "errors" in data
    assert "email" in data["errors"][0]
