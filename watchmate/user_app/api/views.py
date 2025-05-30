from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from user_app.api.serializers import RegistrationSerializer
from user_app import models

@api_view(['POST',])
def logout_view(request):
    
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    

@api_view(['POST',])
@permission_classes([AllowAny])          # ← this lets unauthenticated users in
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()

            data['response'] = 'Registration successful!'
            data['username'] = account.username
            data['email'] = account.email
            
            token = Token.objects.get(user=account).key 
            data['token'] = token
            '''
            refresh = RefreshToken.for_user(account)
            data['token'] =  {
                                'refresh': str(refresh),
                                'access': str(refresh.access_token),
                                }
            '''
        else:
            data = serializer.errors
        
        return Response(data, status=status.HTTP_201_CREATED) 
        