from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')
    list_per_page = 25
