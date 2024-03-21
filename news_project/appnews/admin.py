from django.contrib import admin

# Register your models here.
from .models import Author, Category, Comment, Post, PostCategory

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Author)
