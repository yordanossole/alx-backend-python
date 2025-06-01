# chats/models.py

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model. Currently identical to AbstractUser,
    but you can add fields like avatar, bio, phone_number, etc.
    e.g.:

        bio = models.TextField(blank=True, null=True)
        avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    """
    # (If you want to add any new fields, do it here.)
    # e.g.:
    # bio = models.TextField(blank=True)
    # avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.username




class Conversation(models.Model):
    """
    Represents a chat thread between two or more users.
    """
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations',
        help_text='Users participating in this conversation'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # If you want a simple string, you could list usernames separated by commas:
        names = ", ".join([user.username for user in self.participants.all()])
        return f"Conversation ({names})"

    class Meta:
        ordering = ['-created_at']



class Message(models.Model):
    """
    Represents a single message sent by a user in a conversation.
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text='Conversation this message belongs to'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text='User who sent this message'
    )
    content = models.TextField(help_text='Body of the message')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # e.g. "alice → [conversation id]: Hi there!"
        return f"{self.sender.username} @ {self.timestamp:%Y-%m-%d %H:%M}: {self.content[:30]}…"

    class Meta:
        ordering = ['timestamp']



class User(AbstractUser):
    """
    Custom user model. Extend AbstractUser with any extra fields.
    """
    # Example extra fields (uncomment if you want them):
    # bio = models.TextField(blank=True, null=True)
    # avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.username


class Conversation(models.Model):
    """
    A chat thread between two or more users.
    """
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations',
        help_text='Users participating in this conversation'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # List participant usernames, e.g. "alice, bob"
        names = ", ".join([user.username for user in self.participants.all()])
        return f"Conversation ({names})"

    class Meta:
        ordering = ['-created_at']


class Message(models.Model):
    """
    A single message within a conversation.
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text='Conversation this message belongs to'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text='User who sent this message'
    )
    content = models.TextField(help_text='Body of the message')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} @ {self.timestamp:%Y-%m-%d %H:%M}: {self.content[:30]}…"

    class Meta:
        ordering = ['timestamp']
