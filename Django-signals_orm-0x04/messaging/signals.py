# signals.py
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification
User = get_user_model()

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


@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Performs additional cleanup after a user is deleted.
    This is needed for cases where CASCADE delete might not handle everything,
    or where we want to perform additional actions.
    """
    # Cleanup any notifications where the user was the receiver
    # (handled by CASCADE, but shown here as an example)
    Notification.objects.filter(message__receiver=instance).delete()
    
    # Cleanup any message history where the user was the editor
    MessageHistory.objects.filter(edited_by=instance).delete()
    
    # In a real app, you might also want to:
    # - Delete files uploaded by the user
    # - Send a confirmation email
    # - Log the deletion


@receiver(pre_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Performs additional cleanup after a user is deleted.
    This is needed for cases where CASCADE delete might not handle everything,
    or where we want to perform additional actions.
    """
    # Cleanup any notifications where the user was the receiver
    # (handled by CASCADE, but shown here as an example)
    Notification.objects.filter(message__receiver=instance).delete()
    
    # Cleanup any message history where the user was the editor
    MessageHistory.objects.filter(edited_by=instance).delete()
    
    # In a real app, you might also want to:
    # - Delete files uploaded by the user
    # - Send a confirmation email
    # - Log the deletion