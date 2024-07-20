from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from unittest.mock import patch
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import UserModel, ConfirmationModel, CODE_VERIFIED




class SignUpCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        # Updated to match the URL pattern name
        self.url = reverse('users:register')

    def test_signup_success(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'country': 'Testland'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('access_token' in response.data)
        self.assertEqual(response.data['message'].strip(
        ), "Successfully registered, code sent to you email.")
        print("\rPass !..")



    def test_signup_password_mismatch(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'confirm_password': 'password456',
            'country': 'Testland'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertIn('password', response.data['message'])
        self.assertEqual(response.data['message']
                         ['password'], "Passwords don't match")
        print("\rPass !..")



    def test_signup_invalid_email(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalid-email',
            'password': 'password123',
            'confirm_password': 'password123',
            'country': 'Testland'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertIn('email', response.data['message'])
        self.assertEqual(
            response.data['message']['email'], 'Please enter a valid email address.')
        print("\rPass !..")


    def test_signup_existing_email(self):
        UserModel.objects.create_user(
            username='existinguser',
            email='john.doe@example.com',
            password='password123'
        )
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'country': 'Testland'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertIn('email', response.data['message'])
        self.assertEqual(response.data['message']
                         ['email'], 'Email already exists.')
        print("\rPass !..")








class LoginViewTestCase(APITestCase):
    def setUp(self):
        # Ensure this matches your URL pattern name
        self.url = reverse('users:login')
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            phone_number='+1234567890'
        )


    def test_login_with_username(self):
        data = {
            'userinput': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access_token' in response.data)
        self.assertTrue('refresh_token' in response.data)
        print("\rPass !..")
        


    def test_login_with_email(self):
        data = {
            'userinput': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access_token' in response.data)
        self.assertTrue('refresh_token' in response.data)
        print("\rPass !..")


    def test_login_with_phone_number(self):
        data = {
            'userinput': '+1234567890',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access_token' in response.data)
        self.assertTrue('refresh_token' in response.data)
        print("\rPass !..")


        
    def test_login_invalid_credentials(self):
        data = {
            'userinput': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('success', response.data)
        self.assertEqual(response.data['success'][0], 'False')
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'][0], 'Invalid username or password')
        print("\rPass !..")



class RefreshTokenViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('users:refresh')
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.refresh = RefreshToken.for_user(self.user)

    def test_refresh_token(self):
        data = {
            'refresh': str(self.refresh)
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        print("\rPass !..")




class LogOutViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('users:logout')
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client.force_authenticate(user=self.user)

    def test_logout(self):
        data = {
            'refresh': str(self.refresh)
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['message'], "User logged out successfully")
        print("\rPass !..")

    def test_logout_invalid_token(self):
        data = {
            'refresh': 'invalidtoken'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['success'], False)
        print("\rPass !..")




class CodeVerifiedAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('users:verify')
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)
        self.verification_code = ConfirmationModel.objects.create(
            code='123456',
            is_confirmed=False,
            user=self.user,
            expiration_time=timezone.now() + timezone.timedelta(minutes=10)
        )

    def test_code_verification_success(self):
        data = {
            'code': '123456'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['auth_status'], CODE_VERIFIED)
        print("\rPass !..")

    def test_code_verification_invalid_code(self):
        data = {
            'code': 'invalidcode'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], "Verification code is not valid")
        print("\rPass !..")




class UserUpdateAPIViewTest(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
            phone_number='1234567890',
            bio='This is a test bio',
            age=30,
            country='Testland'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('users:update') 
        print("\rPass !..")

    def test_update_user_success(self):
        data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'username': 'updateduser',
            'phone_number': '0987654321',
            'bio': 'This is an updated bio',
            'age': 31,
            'country': 'Updatedland'
        }
        response = self.client.put(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'User updated successfully')
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.username, 'updateduser')

    def test_partial_update_user_success(self):
        data = {
            'first_name': 'PartiallyUpdated'
        }
        response = self.client.patch(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'User updated successfully')
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'PartiallyUpdated')

    def test_update_user_invalid_data(self):
        data = {
            'first_name': 'Updated123',  # Invalid first name
            'last_name': 'User',
            'username': 'updateduser',
            'phone_number': '0987654321',
            'bio': 'This is an updated bio',
            'age': 31,
            'country': 'Updatedland'
        }
        response = self.client.put(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['success'][0]), 'False')
        self.assertIn('first_name', response.data['message'])
