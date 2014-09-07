from django.contrib import admin
from models import ApiUser


class ApiUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', )
    search_fields = ['user__email', 'user__username']
admin.site.register(ApiUser, ApiUserAdmin)
