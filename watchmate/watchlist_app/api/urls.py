from django.urls import path, include 
#from watchlist_app.api.views import movie_list,movie_details
from watchlist_app.api.views import WatchListAV,WatchDetailAV,ReviewList,ReviewDetail,ReviewCreate,StreamPlatformVS
#from watchlist_app.api.views import StreamPlatformDetailAV,StreamPlatformAV
#from watchlist_app import * 
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('stream',StreamPlatformVS, basename = 'streamplatform')

urlpatterns = [
    path('list/', WatchListAV.as_view(),name='movie-list'),
    path('<int:pk>',WatchDetailAV.as_view(),name = 'movie-details'),
    
    path('',include(router.urls)),
    #path('stream/',StreamPlatformAV.as_view(),name='stream'),
    #path('stream/<int:pk>',StreamPlatformDetailAV.as_view(),name='stream-detail'),
    
    #path('review',ReviewList.as_view(),name='review-list'),
    #for individual review
    #path('review/<int:pk>',ReviewDetail.as_view(),name='review-detail')
    
    #the below url reviews for a particular movie
    #path('stream/<int:pk>/review',StreamPlatformDetailAV.as_view(),name='stream-detail'),

    
    #first url below for reviews for particular movie
    path('stream/<int:pk>/review',ReviewList.as_view(),name='review-list'),
    path('stream/<int:pk>/review-create',ReviewCreate.as_view(),name='review-create'),
    
    path('stream/review<int:pk>/',ReviewDetail.as_view(),name='review-detail'),

]