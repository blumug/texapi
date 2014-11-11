from django.contrib import admin
from models import Text


class TextAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_id', 'url', 'user')
    search_fields = ['url', ]
    list_filter = ['status', ]
admin.site.register(Text, TextAdmin)
