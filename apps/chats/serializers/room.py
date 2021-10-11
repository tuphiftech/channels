from rest_framework import serializers

class RoomSerializer(serializers.Serializer):
    name = serializers.CharField()
    label = serializers.CharField()