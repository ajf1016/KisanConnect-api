# market/admin.py

from django.contrib import admin
from .models import ChatRoom


class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'farmer', 'created_at')
    search_fields = ('buyer__username', 'farmer__username')
    list_filter = ('created_at',)


admin.site.register(ChatRoom, ChatRoomAdmin)
