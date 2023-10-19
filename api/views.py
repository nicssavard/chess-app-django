from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer, MessageSerializer, ChatSerializer
from django.contrib.auth import authenticate
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import Chat, Message
from django.shortcuts import get_list_or_404
from rest_framework import  viewsets
from django.http import JsonResponse

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']     
        )
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
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
    token = request.headers.get('Authorization', '').split(' ')[1]  # Assume the header is 'Bearer <token>'
    try:
        # Decode the token
        untyped_token = UntypedToken(token)
        
        # Get user ID from token payload
        user_id = untyped_token['user_id']
        
        # Fetch the user
        user = User.objects.get(id=user_id)
        serialized_user = UserSerializer(user).data  # Serialize the user object
        # Do something with the user (or simply return it)
        return Response({"user": serialized_user}, status=status.HTTP_200_OK)

    except TokenError as e:
        return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

class UsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['GET'])
def find_chat_by_participants(request):
    participant1_id = int(request.GET.get('participant1_id'))
    participant2_id = int(request.GET.get('participant2_id'))
    if participant1_id is None or participant2_id is None:
        return JsonResponse({'error': 'Both participant1_id and participant2_id must be provided'}, status=400)

    # Your logic to find the chat
    chats = get_list_or_404(Chat, participants__id__in=[participant1_id, participant2_id])
    for chat in chats:
        if set([participant1_id, participant2_id]) == set(chat.participants.values_list('id', flat=True)):
            return JsonResponse({'chat': ChatSerializer(chat).data})

    return JsonResponse({'error': 'Chat not found'}, status=404)
    
@api_view(['GET'])
def test(request):
    return Response({"message": "test"}, status=status.HTTP_200_OK)
