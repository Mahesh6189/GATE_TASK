from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class AccountsTestCase(APITestCase):

    def setUp(self):
        self.register_url = "/api/register/"
        self.login_url = "/api/login/"

        self.user_data = {
            "username": "testuser",
            "password": "testpass123"
        }

        # create a user for login test
        self.user = User.objects.create_user(
            username="existinguser",
            password="existingpass123"
        )

    # ---------------------
    # REGISTER TEST
    # ---------------------
    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "User created")

    # ---------------------
    # LOGIN TEST (SUCCESS)
    # ---------------------
    def test_user_login_success(self):
        response = self.client.post(self.login_url, {
            "username": "existinguser",
            "password": "existingpass123"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Login success")

    # ---------------------
    # LOGIN TEST (FAIL)
    # ---------------------
    def test_user_login_failure(self):
        response = self.client.post(self.login_url, {
            "username": "wronguser",
            "password": "wrongpass"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Invalid credentials")