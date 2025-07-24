import pytest
from rest_framework.test import APIClient
from django.urls import reverse

REGISTER_URL = reverse("register")  # Update with actual path name

client = APIClient()

@pytest.mark.django_db
def test_valid_registration_with_email():
    payload = {
        "phone_number": "+919876543210",
        "name": "Test User",
        "password": "securepass123",
        "email": "user@example.com"
    }
    response = client.post(REGISTER_URL, payload, format="json")
    assert response.status_code == 201
    assert response.data["message"] == "User registered successfully"


@pytest.mark.django_db
def test_valid_registration_without_email():
    payload = {
        "phone_number": "+919876543211",
        "name": "No Email User",
        "password": "securepass456"
    }
    response = client.post(REGISTER_URL, payload, format="json")
    assert response.status_code == 201
    assert response.data["message"] == "User registered successfully"


def test_invalid_phone_format():
    payload = {
        "phone_number": "9876543210",  # missing +91
        "name": "Bad Phone",
        "password": "badpass123",
        "email": "test@example.com"
    }
    response = client.post(REGISTER_URL, payload, format="json")
    assert response.status_code == 400
    assert "Invalid phone number format" in response.data["error"]


def test_invalid_email_format():
    payload = {
        "phone_number": "+919876543210",
        "name": "Bad Email",
        "password": "badpass123",
        "email": "not-an-email"
    }
    response = client.post(REGISTER_URL, payload, format="json")
    assert response.status_code == 400
    assert "Invalid email format" in response.data["error"]


@pytest.mark.django_db
def test_missing_required_fields():
    payload = {
        "phone_number": "+919876543212"
        # Missing name and password
    }
    response = client.post(REGISTER_URL, payload, format="json")
    assert response.status_code == 400
    assert "name" in response.data
    assert "password" in response.data


@pytest.mark.django_db
def test_duplicate_phone_number():
    payload = {
        "phone_number": "+919999999999",
        "name": "User1",
        "password": "pass123"
    }
    response1 = client.post(REGISTER_URL, payload, format="json")
    assert response1.status_code == 201

    response2 = client.post(REGISTER_URL, payload, format="json")
    assert response2.status_code == 400
    assert "phone_number" in response2.data
