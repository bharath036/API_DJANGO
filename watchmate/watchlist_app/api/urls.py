from django.urls import path, include 
from watchlist_app.api.views import movie_list,movie_details
#from watchlist_app import * 

urlpatterns = [
    path('list/', movie_list,name='movie-list'),
    path('<int:pk>',movie_details,name = 'movie-details')
]