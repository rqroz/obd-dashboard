from django.contrib import admin

from backend.models.users import UserDetails


@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    ordering = ['user__first_name', 'user__last_name', 'user__email']
