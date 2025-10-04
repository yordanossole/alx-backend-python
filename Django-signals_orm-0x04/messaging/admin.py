# admin.py
from django.contrib import admin
from .models import Message, MessageHistory, Notification

class MessageHistoryInline(admin.TabularInline):
    model = MessageHistory
    extra = 0
    readonly_fields = ('edited_at', 'edited_by', 'old_content')
    can_delete = False

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'edited', 'last_edited')
    list_filter = ('edited', 'timestamp')
    search_fields = ('content', 'sender__username', 'receiver__username')
    inlines = [MessageHistoryInline]

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')