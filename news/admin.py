from django.contrib import admin
from . import models


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    pass
