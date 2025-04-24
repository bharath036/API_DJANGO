'''
from django.shortcuts import render
from watchlist_app.models import * 
from django.http import JsonResponse 

# Create your views here.

def movie_list(request):
    
    #We will get all movies in movie table
    movies = Movie.objects.all()
    #We can't return them directly, we need to return in json format
    #print(movies.values())
    data = {
        'movies' : list(movies.values())
    }
    
    return JsonResponse(data)

#Lets extract info for particular object, for this we need to write url for it specific object
def movie_details(request,pk): #pk is id or any id for particualr object or record, url looks like this http://127.0.0.8000/movie/1 --> 1 is pk that can be changed
    movie = Movie.objects.get(pk=pk)
    #print(movie)
    data = {
        'name': movie.name,
        'description' : movie.description,
        'active':movie.active
    }
    return JsonResponse(data)
    

'''