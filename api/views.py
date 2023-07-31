from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Q
from rest_framework import serializers
import json
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

class MessagesByRoomView(APIView):
    def get(self, request, room_id):
        # messages = Message.objects.all().values()
        messages = Message.objects.filter(Q(room__id=room_id))
        print(messages)
        serializer = MessageSerializer(messages, many=True)
        # data = serializers.Serialize
        print(serializer.data)
        dictionary = {
            'name': 'Bard',
            'age': 18,
            'hobbies': ['coding', 'playing guitar', 'reading'],
        }

        # json_data = json.dumps(messages)
        print("hello")
        room = Room.objects.get(id=room_id)
        room_messages = room.message_set.all()
        room_messages = serializers.Serializer(room_messages).data
        print(room)
        
        print("done")
        e = {"error":"error"}
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserloginView(APIView):
    queryset = User.objects.all()
    serializer_class = UserloginSerializer
    def get(self, request):
        # Your logic for handling GET requests goes here
        data = {'message': 'This is a GET request.'}
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        # Your logic for handling POST requests goes here
        data = request.data 
        # Request data sent by the client
        serializer = UserloginSerializer(data=request.data)
        if serializer.is_valid():
            username = data.get('username')
            password = data.get('password')
            redirect_url = reverse('token_obtain_pair')+f'?username={username}&password={password}'
            return HttpResponseRedirect(redirect_url)

        # Process the data and do something with it
        return Response(data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        # Your logic for handling PUT requests goes here
        data = request.data
        # Process the data and update the corresponding object
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        # Your logic for handling DELETE requests goes here
        # Delete the corresponding object
        return Response({'message': 'Object deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def perform_create(self, serializer):
        print("view class")
        print(serializer.validated_data)
        print("view end")
        # serializer.save()

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    # permission_classes = [IsAuthenticated]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
