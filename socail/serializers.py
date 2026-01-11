from rest_framework import serializers
from .models import MessengerMessage

class MessengerMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessengerMessage
        fields = ['id', 'sender_id', 'message_text', 'timestamp']
        