# signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Logs the previous content of a message before it's edited.
    """
    if instance.pk:  # Only for existing messages (edits)
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:  # Only log if content changed
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content,
                    edited_by=instance.sender
                )
                instance.edited = True
                instance.last_edited = timezone.now()
        except Message.DoesNotExist:
            pass

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Creates a notification for the receiver when a new message is sent.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )