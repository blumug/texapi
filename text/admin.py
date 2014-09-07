from django.contrib import admin
from models import Text


class TextAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'user')
    search_fields = ['url', ]
admin.site.register(Text, TextAdmin)
