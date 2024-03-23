from django.contrib import admin

# Register your models here.
from .models import Author, Category, Comment, Post, PostCategory


class AutorAdmin(admin.ModelAdmin):
    list_display = ('id', 'pk', 'authorUser', 'ratingAuthor')
    list_filter = ('authorUser', 'ratingAuthor')
    search_fields = ('authorUser__username', 'ratingAuthor')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'pk', 'name')
    list_filter = ('name',)
    search_fields = ('name',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'pk', 'author', 'categoryType', 'dateCreation', 'title', 'preview', 'rating')
    list_filter = ('author', 'categoryType', 'dateCreation', 'rating')
    search_fields = ('author__authorUser__username', 'title', 'categoryType')


def nullfy_rating(modeladmin, request, queryset):
    queryset.update(rating=0)


def app_rating(modeladmin, request, queryset):
    queryset.update(rating=100)


nullfy_rating.short_description = 'Обнулить рейтинг комментария'
app_rating.short_description = 'Установить рейтинг комментария на 100'


class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.get_fields()]
    actions = [nullfy_rating, app_rating]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Author, AutorAdmin)
