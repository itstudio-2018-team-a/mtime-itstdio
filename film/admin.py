from django.contrib import admin

from . import models


@admin.register(models.Tags)
class TagsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Film)
class FilmAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Mark)
class MarkAdmin(admin.ModelAdmin):
    pass


@admin.register(models.OnMovie)
class OnMovieAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ComingMovie)
class ComingMovieAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FilmComment)
class FilmCommentAdmin(admin.ModelAdmin):
    list_display = ('film', 'create_time', 'update_time')
    pass


@admin.register(models.FilmReview)
class FilmReviewAdmin(admin .ModelAdmin):
    pass


@admin.register(models.FilmReviewComment)
class FilmReviewCommentAdmin(admin.ModelAdmin):
    pass

