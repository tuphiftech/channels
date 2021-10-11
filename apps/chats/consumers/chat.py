# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework import serializers
from ..models import Message, Room
from ..serializers import MessageSerializer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        self.room, created = Room.objects.get_or_create(label=self.room_name)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        get_all_messages = text_data_json.get("get_all_messages")


        if get_all_messages == True:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'all_messages',
                }
            )
        else:
            # Save message to DB
            message = text_data_json['message']
            message_object = Message(room=self.room, message=message)
            message_object.save()

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
    
    # Receive request get all messages
    def get_all_messages(self):
        all_messages = Message.objects.filter(room=self.room)
        all_messages_data = MessageSerializer(all_messages, many=True).data
        return all_messages_data
    
    def all_messages(self, event):
        result_messages = {
            'all_messages': self.get_all_messages(),
            'send_all_messages': True
        }
        self.send(text_data=json.dumps(result_messages))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))