# views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message, MessageHistory

@login_required
def message_history(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    
    # Verify the user has permission to view this message history
    if request.user not in [message.sender, message.receiver]:
        return HttpResponseForbidden("You don't have permission to view this message history")
    
    history = message.history.all().order_by('-edited_at')
    
    return render(request, 'message_history.html', {
        'message': message,
        'history': history
    })