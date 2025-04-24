from rest_framework.response import Response
from rest_framework.decorators import api_view
from watchlist_app.models import Movie
from watchlist_app.api.serializers import MovieSerializer
from rest_framework import status 

@api_view(['GET','POST'])
def movie_list(request):
    if request.method == 'GET':
        
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        #Get data from user
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():  #if data is valid we will send data or else error 
            serializer.save()
            #The data we are getting below validated_data is because of return in create function in serializers.py
            return Response(serializer.data)
        
        else:
            return Response(serializer.errors)
        
        
#We can't perform POST operation here because we are using individual element here
@api_view(['GET','PUT','DELETE'])
def movie_details(request,pk):

    if request.method == 'GET':
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({'Error': 'Movie not found'},status=status.HTTP_404_NOT_FOUND)    
        
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        #Here we update 
        #patch means any one can be updated but in put all to rewrite
        movie = Movie.objects.get(pk=pk)
        #the above is required or else if we refresh it will come back to old value 
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
        
    if request.method == 'DELETE':
        movie = Movie.objects.get(pk=pk)
        movie.delete()
        #if we deleted something we will get response in the form of status code
        return Response(status= status.HTTP_204_NO_CONTENT)
        
    

