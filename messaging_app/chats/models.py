# chats/models.py

import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model with a UUID primary key and explicit email/first_name/last_name fields.
    """
    # Replace the default integer-based PK with a UUID
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Redefine email, first_name, last_name explicitly (AbstractUser already has them,
    # but we declare them here to satisfy the schema-check requirements).
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=150)

    # (password is inherited from AbstractUser as a CharField; no need to re-declare it.)
    # If you want to enforce email as the username field, you could add:
    #     USERNAME_FIELD = 'email'
    #     REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    # but leaving username-based login is also fine if you prefer.

    def __str__(self):
        return self.email or self.username


class Conversation(models.Model):
    """
    Tracks which users are involved in a conversation.
    """
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations',
        help_text='Users participating in this conversation'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Show all participant emails/usernames for readability
        names = ", ".join([user.email or user.username for user in self.participants.all()])
        return f"Conversation ({names})"

    class Meta:
        ordering = ['-created_at']


class Message(models.Model):
    """
    Contains the sender, conversation, message body, and timestamp.
    """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Explicitly name the ForeignKey as conversation_id so the column is named accordingly
    conversation_id = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        db_column='conversation_id',
        help_text='Conversation this message belongs to'
    )

    # The sender: links to User (whose PK is user_id)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text='User who sent this message'
    )

    # The actual body of the message
    message_body = models.TextField(help_text='Body of the message')

    # Timestamp when the message was sent
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        preview = self.message_body[:30] + ("…" if len(self.message_body) > 30 else "")
        return f"{self.sender.email or self.sender.username} @ {self.sent_at:%Y-%m-%d %H:%M}: {preview}"

    class Meta:
        ordering = ['sent_at']
