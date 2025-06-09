# views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message, MessageHistory
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

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


@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # Logout before deleting to prevent issues
        user.delete()  # This will trigger the post_delete signal
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('home')
    return render(request, 'accounts/confirm_delete.html')