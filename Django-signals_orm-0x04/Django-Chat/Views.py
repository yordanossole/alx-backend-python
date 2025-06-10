# Django-Chat/Views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden

User = get_user_model()

@login_required
def delete_user(request):
    """
    View to handle user account deletion with confirmation.
    """
    if request.method == 'POST':
        # Additional confirmation check
        if request.POST.get('confirmation') != 'DELETE':
            messages.error(request, 'Please type DELETE to confirm account deletion.')
            return render(request, 'accounts/confirm_delete.html')
        
        # Get the user and logout before deletion
        user = request.user
        logout(request)
        
        try:
            # Delete the user (this will trigger the post_delete signal)
            user.delete()
            messages.success(request, 'Your account has been successfully deleted.')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'An error occurred while deleting your account: {str(e)}')
            return redirect('profile')
    
    # GET request - show confirmation page
    return render(request, 'accounts/confirm_delete.html')