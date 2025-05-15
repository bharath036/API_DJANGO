from django.test import TestCase
#from django.test import TestCase
from django.contrib.auth.models import User 
from rest_framework.test import APITestCase

from django.urls import reverse
from rest_framework import status

from rest_framework.authtoken.models import Token 
# Create your tests here.

class RegisterTestCae(APITestCase):

    #for now let's create one test case
    #while running testcases django will create new db temporary and run there. There won't be any effect to our test case
    def test_register(self):
        data = {
            "username": "testcase",
            "email" : "testcase@example.com",
            "password": "NewPassword",
            "password2": "NewPassword"
        }

        #sending client request, in post we pass url, data
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


#LOGIN & LOGOUT TESTCASE

class LoginLogoutTestCase(APITestCase):
    #We need to create fake user to test
    def setUp(self):
        self.user = User.objects.create_user(username="example",password="NewPassword")

    def test_login(self):
        data = {
            "username" : "example",
            "password" : "NewPassword"
        }

        response = self.client.post(reverse('login'),data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        #to logout we need to sendout token 
        self.token = Token.objects.get(user__username="example")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


