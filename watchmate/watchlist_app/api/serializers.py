#We will map all the values step by step
#First step we will map by rest framework 

from rest_framework import serializers
from watchlist_app.models import Movie

#This serializers will map all values
#We will add validations, add methods etc inside this 
class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField()
    description = serializers.CharField()
    active = serializers.BooleanField()
    
    def create(self, validated_data):

        return Movie.objects.create(**validated_data)
    
    #instance old updated with new
    def update(self, instance,validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.description = validated_data.get('name',instance.description)
        instance.active = validated_data.get('name',instance.active)
        instance.save()
        return instance  