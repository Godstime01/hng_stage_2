import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from auth_core.models import UserModel
from api.models import Organisation


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "password": "password123",
    }


@pytest.mark.django_db
class TestUserRegistration:

    def test_registration_url(self):
        url = reverse("register")
        assert url == "/auth/register/"

    def test_registration_success(self, client, user_data):
        url = reverse("register")
        response = client.post(url, data=user_data, format="json")
        print(response.data)

        assert response.status_code == 201

        assert response.data["status"] == "success"
        assert response.data["message"] == "Registration successful"
        assert "data" in response.data
        assert "accessToken" in response.data["data"]

    def test_missing_username(self, client, user_data):
        # Remove username from user_data to simulate missing required field
        user_data.pop("first_name", None)
        url = reverse("register")
        response = client.post(url, data=user_data, format="json")

        assert response.status_code == 422

    def test_existing_email(self, client, user_data):
        # Create a user with the same username as in user_data
        UserModel.objects.create_user(
            first_name="rand",
            last_name="user",
            phone="+1234567890",
            email=user_data["email"],
            password="testpassword",
        )

        url = reverse("register")
        response = client.post(url, data=user_data, format="json")

        assert response.status_code == 422

    def test_unsuccesful_registration(self, client, user_data):
        # Remove password from user_data to simulate unsuccessful registration
        url = reverse("register")
        response = client.post(url, format="json")

        assert response.status_code == 422
        assert response.data["status"] == "Bad request"
        assert response.data["message"] == "Registration unsuccessful"
        assert response.data["statusCode"] == 400


@pytest.mark.django_db
class TestUserLogin:

    def test_login_url_is_correct(self):
        url = reverse("login")
        assert url == "/auth/login/"

    def test_login_success(self, client, user_data):
        # Create a user with the same username as in user_data
        user = UserModel.objects.create_user(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=user_data["password"],
        )

        url = reverse("login")
        response = client.post(url, data=user_data, format="json")

        assert response.status_code == 200
        assert response.data["status"] == "success"
        assert response.data["message"] == "Login successful"
        assert "data" in response.data
        assert "accessToken" in response.data["data"]
        assert "user" in response.data["data"]

    def test_login_unsuccessful(self, client, user_data):
        url = reverse("login")
        response = client.post(
            url,
            data={"email": user_data["email"], "password": "wrongpassword"},
            format="json",
        )

        assert response.status_code == 401
        assert response.data["status"] == "Bad request"
        assert response.data["message"] == "Authentication failed"
