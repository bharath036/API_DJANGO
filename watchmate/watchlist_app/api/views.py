from rest_framework.response import Response
#from rest_framework.decorators import api_view
from rest_framework.views import APIView
from watchlist_app.models import StreamPlatform,WatchList,Review
from watchlist_app.api.serializers import WatchListSerializer,StreamPlatformSerializer,ReviewSerializer
from rest_framework import status 
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from watchlist_app.api.permissions import IsAdminOrReadOnly,ReviewUserOrReadOnly

from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from watchlist_app.api.throttling import *

class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    #permission_classes = [IsAuthenticatedOrReadOnly] #only authenticated user can use this
    #permission_classes = [IsAuthenticated]
    #throttle_classes = [ReviewListThrottle,AnonRateThrottle]
    
    def get_queryset(self):
        username = self.kwargs['username']
        return Review.objects.filter(review_user__username=username)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_class = [ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self,serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        
        review_user = self.request.user 
        review_queryset = Review.objects.filter(watchlist=movie,review_user=review_user)
        #if anyone is reviewed we get below error
        if review_queryset.exists():
            raise ValidationError("You have already reviewd this movie!")
        
        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else: #we need to calculate rating old and new rating average
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating'])/2
            
        movie.number_rating = movie.number_rating +1
        movie.save()
        
        serializer.save(watchlist=movie,review_user=review_user)
        

class ReviewList(generics.ListAPIView):
    #the below gives all reviews 
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #permission_classes = [IsAuthenticatedOrReadOnly] #only authenticated user can use this
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle,AnonRateThrottle]
    #below says that we are going to filter but for what fields to filter?
    filter_backends = [DjangoFilterBackend]
    #what fields to filter
    filterset_fields = ['review_user__username', 'active']
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticatedOrReadOnly]
    #permission_classes = [AdminOrReadOnly]
    permission_classes = [ReviewUserOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

'''
#We created this reviewlist class , mixins import followed by this we imported Generics
class ReviewList(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 generics.GenericAPIView):
    
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer 
    
    def get(self,request,*args,**kwargs):
            return self.list(request,*args,**kwargs)
        
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    
class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
'''
#The below viewsets has several methods (VS we used in class name means viewsets)
class StreamPlatformVS(viewsets.ViewSet):
    
    def list(self, request):
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk=None):
        queryset = StreamPlatform.objects.all()
        watchlist = get_object_or_404(queryset,pk=pk)
        serializer = StreamPlatformSerializer(StreamPlatform)
        return Response(serializer.data)
    
    #post request  oprion
    def create(self,request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
#Updated model serializer views
class StreamPlatformAV(APIView):
    
    def get(self,request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform,many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

#viewset class 
class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    

'''     
class StreamPlatformDetailAV(APIView):
    
    def get(self,request,pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Not found'},status=status.HTTP_404_NOT_FOUND)    
        
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)
        
        
    def put(self,request,pk):
        movie = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
    def delete(self,request,pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)
'''

class WatchListGV(generics.ListAPIView):
    #the below gives all reviews 
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #permission_classes = [IsAuthenticatedOrReadOnly] #only authenticated user can use this
    #below says that we are going to filter but for what fields to filter?
    filter_backends = [DjangoFilterBackend]
    #what fields to filter
    filterset_fields = ['title', 'platform__name']

#Class Based View
class WatchListAV(APIView):
    
    def get(self,request):
        movies = WatchList.objects.all()
        serialzer = WatchListSerializer(movies, many = True)
        return Response(serialzer.data)
    
    def post(self,request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

        
        
class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]
    
    def get(self,request,pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Not found'},status=status.HTTP_404_NOT_FOUND)    
        
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
        
        
    def put(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
    def delete(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)
        
             
    

'''
#Function based class
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
        
    

'''