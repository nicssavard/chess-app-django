from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.models import User

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    print('login')
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user:
        # Create a JWT token
        refresh = RefreshToken.for_user(user)
        serialized_user = UserSerializer(user).data  # Serialize the user object
        
        return Response({
            'message': 'Successful login',
            'user': serialized_user,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })
    
    return Response({"message": "Login failed"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_user_from_token(request):
    print('tkejkljcdklsajfdkl')
    token = request.headers.get('Authorization', '').split(' ')[1]  # Assume the header is 'Bearer <token>'
    print(token)
    try:
        # Decode the token
        untyped_token = UntypedToken(token)
        
        # Get user ID from token payload
        user_id = untyped_token['user_id']
        
        # Fetch the user
        user = User.objects.get(id=user_id)
        serialized_user = UserSerializer(user).data  # Serialize the user object
        print('test')
        print(user.id)
        print(user)
        # Do something with the user (or simply return it)
        return Response({"user": serialized_user}, status=status.HTTP_200_OK)

    except TokenError as e:
        return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
    


class UsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    