# urls.py
from django.urls import path
from .views import message_history

urlpatterns = [
    # ... other URLs ...
    path('messages/<int:message_id>/history/', message_history, name='message_history'),
]