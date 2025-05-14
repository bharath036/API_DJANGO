#We will map all the values step by step
#First step we will map by rest framework 

from rest_framework import serializers
from watchlist_app.models import WatchList,StreamPlatform,Review 

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only = True)
    
    class Meta:
        model = Review 
        fields = "__all__"
    
    
#Modelserializer have create,update all things, we need not create update,create methods manually as previously
#For validators we need to add inside class separately as this model serializer won't take care of it
#Here we see about model serializer 
class WatchListSerializer(serializers.ModelSerializer):
    #len_name = serializers.SerializerMethodField()
    platform = serializers.CharField(source='platform.name')
    #reviews = ReviewSerializer(many=True, read_only = True)
    class Meta:
        model = WatchList
        #instea=d of all we can pass particular columns
        #fields = "__all__", orselse we can use exclude = ['active']
        #fields = ['id','name','description']
        fields = "__all__"
        
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    #To see the platform containg that movies , what movies it has 
    #One streaming platform can have any number of movies but one movie has one streaming platform
    #watchlist = WatchListSerializer(many=True,read_only=True)
    #serializer relations down line
    watchlist = serializers.StringRelatedField(many=True)
    #or else if we want only primay key that also we can return, or hyperlink also
    
    class Meta:
        model = StreamPlatform
        fields = "__all__"
    

        
        
    
    
'''
def name_length(value):
    if len(value) < 2:
        raise serializers.ValidationError("Name is too short!")


#This serializers will map all values
#We will add validations, add methods etc inside this 
class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField(validators = [name_length])
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
    
    
    #Object level validation
    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError("Title and description should be diffwerent")
        else:
            return data  
'''
    
'''
    #the below is field level validation particular column in table
    def validate_name(self,value):
        
        if len(value) < 2:
            raise serializers.ValidationError("Name is too short!")
        else:
            return value 
        
'''