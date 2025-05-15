from django.test import TestCase
#from django.test import TestCase
from django.contrib.auth.models import User 
from rest_framework.test import APITestCase

from django.urls import reverse
from rest_framework import status

from rest_framework.authtoken.models import Token 
from watchlist_app.api import serializers
from watchlist_app import models

class StreamPlatfromTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example",password="NewPassword")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                           about = "#1 Platform", website = "https://www.netflix.com")

    def test_streamplatfrom_create(self):
        #sending this data without logged in user
        #we get error because this here only admin can send request , so we have to pass 403 instead of 201
        data = {
            "name": "Netflix",
            "about": "#1 Streaming Platform",
            "webside": "https://netflix.com"
        }

        response = self.client.post(reverse('streamplaform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        response = self.client.get(reverse('streamplatform-detail',args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example",password="NewPassword")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                           about = "#1 Platform",
                                                           website = "https://www.netflix.com")
        self.watchlist = models.WatchList.objects.create(platform=self.stream,
                                                         title="Example movie",
                                                         storyline = "Example Movie",
                                                         active = True)

    def test_watchlist_create(self):
        data = {
            "platform" : self.stream,
            "title" : "Example Movie",
            "storyline": "Example Story",
            "active": True 
        }
        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


    def test_watchlist_ind(self):
        response = self.client.get(reverse('movie-detail',args=(self.watchlist.id)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ReviewTestCase(APITestCase):
    
    def setUp(self):
        #created a user
        self.user = User.objects.create_user(username="example",password="NewPassword")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        #created a streamplaform, movie
        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                           about = "#1 Platform",
                                                           website = "https://www.netflix.com")
        self.watchlist = models.WatchList.objects.create(platform=self.stream,
                                                         title="Example movie",
                                                         storyline = "Example Movie",
                                                         active = True)
        self.review = models.Review.objects.create(review_user = self.user,rating =  5,
                                                description= "Great Movie!",
                                                watchlist= self.watchlist,
                                                active= True)

        
    def test_review_create(self):
        data = {
            "review_user" : self.user,
            "rating": 5,
            "description": "Great Movie!",
            "watchlist": self.watchlist,
            "active": True
        }

        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(),1)
        self.assertEqual(models.Review.objects.get().rating,5)

        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_review_create_unauth(self):
        data = {
            "review_user" : self.user,
            "rating": 5,
            "description": "Great Movie!",
            "watchlist": self.watchlist,
            "active": True
        }

        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #update a review, put request
    def test_review_update(self):
        data = {
            "review_user" : self.user,
            "rating": 4,
            "description": "Great Movie!- Updated",
            "watchlist": self.watchlist,
            "active": True
        }
        response = self.client.put(reverse('review-detail', args=(self.review.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get('review-list',args=(self.watchlist.id,))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_ind(self):
        response = self.client.get('review-detail',args=(self.review.id,))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_user(self):
        response = self.client.get('/watch/review/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    



