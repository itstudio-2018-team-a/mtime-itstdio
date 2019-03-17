from django.contrib import admin
from . import models


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'public_time', 'hotpoint',)
    list_per_page = 20
    search_fields = ('title',)
    actions_on_top = True
    ordering = ('-id',)


@admin.register(models.NewsComments)
class NewsCommentsAdmin(admin.ModelAdmin):
    list_display = ('get_news_title', 'get_author_name',)
    list_per_page = 20
    search_fields = ('get_news_title', 'get_author_name',)
    actions_on_top = True


