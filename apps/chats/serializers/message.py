from rest_framework import serializers

class MessageSerializer(serializers.Serializer):
    # room = serializers.IntegerField()
    # handle = serializers.CharField()
    message = serializers.CharField()
    timestamp = serializers.DateTimeField()