from django.contrib import admin

from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_time', 'post']
    fieldsets = [
        ('User', {'fields': ['name', 'email', 'url']}),
        ('Comment', {'fields': ['post', 'text']}),
    ]

# admin.site.register(Comment, CommentAdmin)
