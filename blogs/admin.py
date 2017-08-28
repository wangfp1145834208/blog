from django.contrib import admin
from .models import Post, Category, Tag
from comments.models import Comment

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 5

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
    fieldsets = [
        ('Main', {'fields': ['title', 'author', 'excerpt', 'body']}),
        ('Date information', {'fields': ['created_time', 'modified_time']}),
        ('Other', {'fields': ['category', 'tags']}),
    ]
    inlines = [CommentInline]

#class PostInline(admin.StackedInline):
#    model = Post
#    extra = 3

#class CategoryAdmin(admin.ModelAdmin):
#    inlines = [PostInline]

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
