# messaging_app/chats/serializers.py

from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Conversation, Message

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.
    """
    class Meta:
        model = User
        fields = (
            'user_id',
            'username',
            'email',
            'first_name',
            'last_name',
        )


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message. 
    - The 'sender' field is nested as a UserSerializer (read-only).
    """
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = (
            'message_id',
            'conversation_id',
            'sender',
            'message_body',
            'sent_at',
        )


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation.
    - 'participants' is nested as a list of UserSerializer (read-only).
    - 'messages' is nested as a list of MessageSerializer (read-only).
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = (
            'conversation_id',
            'participants',
            'created_at',
            'messages',
        )
