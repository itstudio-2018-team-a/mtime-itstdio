from django.contrib import admin
from . import models


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(models.NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ('news',)
