from django.shortcuts import render
from .models import Room
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import RoomSerializer, MessageSerializer
from apps.chats import serializers

# Create your views here.
# def chat_room(request, label):
#     # If the room with the given label doesn't exist, automatically create it
#     # upon first visit (a la etherpad).
#     room, created = Room.objects.get_or_create(label=label)

#     # We want to show the last 50 messages, ordered most-recent-last
#     messages = reversed(room.messages.order_by('-timestamp')[:50])

#     return HttpResponse({
#         'room': room,
#         'messages': messages,
#     })


class ChatRoomViewSet(viewsets.ViewSet):
    
    # @action(detail=True, methods=['get'])
    def retrieve(self, request, pk=None):
        room, created = Room.objects.get_or_create(label=pk)
        messages = reversed(room.messages.order_by('-timestamp')[:50])

        result = {
            'room': RoomSerializer(room).data,
            'messages': MessageSerializer(messages, many=True).data
        }
        return Response(data=result, status=status.HTTP_200_OK)

# chat/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })