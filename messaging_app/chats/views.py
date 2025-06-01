# messaging_app/chats/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers  # for raising ValidationError
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

User = get_user_model()


class ConversationViewSet(viewsets.ModelViewSet):
    """
    list, retrieve, create, update, destroy for Conversation.
    - Only returns conversations the authenticated user participates in.
    - On create, expects a list of participant UUIDs (excluding the creator).
      The creator (request.user) will automatically be added if not included.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only conversations where the current user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Expects JSON body:
        {
            "participant_ids": [
                "uuid-of-user-1",
                "uuid-of-user-2",
                ...
            ]
        }
        """
        participant_ids = request.data.get("participant_ids", [])
        if not isinstance(participant_ids, list) or not participant_ids:
            return Response(
                {"detail": "participant_ids must be a non-empty list of user UUIDs."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch users matching the provided UUIDs
        participants = User.objects.filter(user_id__in=participant_ids)
        if participants.count() != len(participant_ids):
            return Response(
                {"detail": "One or more participant_ids are invalid."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the conversation
        convo = Conversation.objects.create()
        # Add requested participants
        convo.participants.add(*participants)

        # Ensure the creator is also a participant
        if request.user not in participants:
            convo.participants.add(request.user)

        serializer = self.get_serializer(convo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    list, retrieve, create, update, destroy for Message.
    - Only returns messages belonging to conversations the user is in.
    - On create, 'sender' is set to request.user automatically.
    - Expects 'conversation_id' (UUID) in the input JSON.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        If a ?conversation_id=<uuid> query param is provided, 
        filter messages to that conversation (only if user is a participant).
        Otherwise, return all messages across all conversations the user is in.
        """
        user = self.request.user
        convo_id = self.request.query_params.get("conversation_id")

        if convo_id:
            return Message.objects.filter(
                conversation_id__conversation_id=convo_id,
                conversation_id__participants=user
            )
        # All messages in any conversation the user participates in:
        return Message.objects.filter(conversation_id__participants=user)

    def perform_create(self, serializer):
        """
        Called when a POST /messages/ is made.
        We need to:
        1. Verify that the provided conversation_id exists.
        2. Verify that request.user is a participant.
        3. Save the message with sender=request.user.
        """
        convo = serializer.validated_data.get("conversation_id")
        if not convo:
            raise serializers.ValidationError({"conversation_id": "This field is required."})

        # Check that the authenticated user is a participant in this conversation
        if self.request.user not in convo.participants.all():
            raise serializers.ValidationError({"detail": "You are not a participant of this conversation."})

        # All good → save with sender=request.user
        serializer.save(sender=self.request.user)
