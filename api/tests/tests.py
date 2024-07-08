import pytest

from django.urls import reverse
from rest_framework.test import APIClient

from ..models import Organisation, UserModel


@pytest.fixture
def create_organisation():
    return Organisation.objects.create(name=None)


class TestOrganinsations:

    def test_get_user_organisation_url(self):
        url = reverse("organisations-list")

        assert url == "/api/organisations/"

    def test_get_user_organisation_detail_url(self):
        url = reverse("organisations-detail", kwargs={"pk": 1})
        assert url == "/api/organisations/1/"

    def test_get_organisation_endpoint(self):
        client = APIClient()
        url = reverse("organisations-list")
        response = client.get(url, format="json")

        assert response.status_code == 200
        assert response.data["status"] == "success"
        assert response.data["message"] == "success"
        assert "organinsations" in response.data["data"]
        assert "orgId" in response.data["data"]["organisations"][0]
        assert "name" in response.data["data"]["organisations"][0]
        assert "description" in response.data["data"]["organisations"][0]

    def test_create_organisation_success(self):
        client = APIClient()
        url = reverse("organisations-list")

        data = {
            "name": "John's Organisation",
        }
        response = client.post(url, data=data, format="json")

        assert response.status_code == 200
        assert response.data["status"] == "success"
        assert response.data["message"] == "success"
        assert "organinsations" in response.data["data"]
        assert "orgId" in response.data["data"]["organisations"][0]
        assert "name" in response.data["data"]["organisations"][0]
        assert "description" in response.data["data"]["organisations"][0]

    def test_create_organisation_failure(self):
        client = APIClient()
        url = reverse("organisations-list")

        data = {
        }

        response = client.post(url, data=data, format="json")

        assert response.status_code == 200
        assert response.data["status"] == "Bad Request"
        assert response.data["message"] == "Client error"
        assert response.data['statusCode'] == 400

    def test_access_organization_details_unauthorized(self):
        user = UserModel.objects.create_user(
            first_name='john',
            last_name='doe',
            email='john.doe@example.com',
            password='password123',
        )
        client = APICli

        assert response.status_code == 403
