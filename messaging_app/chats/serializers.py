# messaging_app/chats/serializers.py

from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Conversation, Message

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.
    - Adds a write-only CharField for password.
    - Overrides create() to set the password properly.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'user_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        )

    def create(self, validated_data):
        # Remove password from validated_data to handle it separately
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            raise serializers.ValidationError("Password is required for user creation.")
        user.save()
        return user


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message.
    - Includes a SerializerMethodField 'short_content' for a truncated preview.
    - Validates that message_body is not blank.
    """
    sender = UserSerializer(read_only=True)
    short_content = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            'message_id',
            'conversation_id',
            'sender',
            'message_body',
            'sent_at',
            'short_content',
        )

    def get_short_content(self, obj):
        # Return the first 50 characters of message_body (or entire body if shorter)
        text = obj.message_body or ""
        return text if len(text) <= 50 else text[:50] + "…"

    def validate_message_body(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Message body cannot be blank.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation.
    - 'participants' is a list of UserSerializer (read-only).
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
