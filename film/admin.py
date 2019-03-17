from django.contrib import admin

from . import models


@admin.register(models.Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'public_time', 'score',)
    list_per_page = 20
    search_fields = ('title',)
    readonly_fields = ('score', 'marking_members', 'commenting_members')
    actions_on_top = True
    ordering = ('-id',)
    list_filter = ('public_time',)
    date_hierarchy = 'public_time'


@admin.register(models.OnMovie)
class OnMovieAdmin(admin.ModelAdmin):
    list_display = ('get_film_title', 'get_film_public_time')
    list_per_page = 20
    search_fields = ('get_film_title',)
    actions_on_top = True


@admin.register(models.ComingMovie)
class ComingMovieAdmin(admin.ModelAdmin):
    list_display = ('get_film_title', 'get_film_public_time',)
    list_per_page = 20
    search_fields = ('get_film_title',)
    actions_on_top = True


@admin.register(models.FilmComment)
class FilmCommentAdmin(admin.ModelAdmin):
    list_display = ('get_film_title', 'get_author_name',)
    list_per_page = 20
    search_fields = ('get_film_title', 'get_author_name',)
    actions_on_top = True


@admin.register(models.FilmReview)
class FilmReviewAdmin(admin.ModelAdmin):
    list_display = ('get_film_title', 'get_author_name',)
    list_per_page = 20
    search_fields = ('get_film_title', 'get_author_name',)
    actions_on_top = True


@admin.register(models.FilmReviewComment)
class FilmReviewCommentAdmin(admin.ModelAdmin):
    list_display = ('get_film_review_title', 'get_film_title', 'get_author_name',)
    list_per_page = 20
    search_fields = ('get_film_review_title', 'get_film_title', 'get_author_name',)
    actions_on_top = True






