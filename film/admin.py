from django.contrib import admin
from django.utils.html import format_html

from . import models
from . import forms


def active_false(self, request, queryset):
    number = queryset.update(active=False)
    return self.message_user(request, number)


active_false.short_description = "禁用"


def active_true(self, request, queryset):
    number = queryset.update(active=True)
    return self.message_user(request, number)


active_true.short_description = "启用"


class FilmCommentInline(admin.TabularInline):
    model = models.FilmComment


class FilmReviewInline(admin.TabularInline):
    model = models.FilmReview


@admin.register(models.Tags)
class TagsAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = ('tag',)


class ScoreFilter(admin.SimpleListFilter):
    title = "评分"
    parameter_name = 'score'

    def lookups(self, request, model_admin):
        return (
            ('8~10', u"8到10分"),
            ('6~8', u"6到8分"),
            ('4~6', u"4到6分"),
            ('0~4', u"小于4分"))

    def queryset(self, request, queryset):
        if self.value() == '8~10':
            return queryset.filter(score__gte=8)
        if self.value() == '6~8':
            return queryset.filter(score__lte=8, score__gte=6)
        if self.value() == '4~6':
            return queryset.filter(score__lte=6, score__gte=4)
        if self.value() == '0~4':
            return queryset.filter(score__lte=4)


@admin.register(models.Film)
class FilmAdmin(admin.ModelAdmin):

    # inlines = [FilmCommentInline, FilmReviewInline]
    list_per_page = 20
    list_display = ('image_data', 'name', 'score')
    list_display_links = ('image_data', 'name')
    list_filter = ((ScoreFilter), 'tag')
    readonly_fields = ('score', 'marked_members', 'commented_member')
    search_fields = ('name',)

    def image_data(self, obj):
        return format_html('<img src="{}" width="25px"/>', obj.head_image.url)
    image_data.short_description = u'封面'

    actions = [active_true, active_false]


@admin.register(models.Mark)
class MarkAdmin(admin.ModelAdmin):
    form = forms.ScoreForm
    list_display = ('film', 'user', 'score')
    search_fields = ('film__name', "user__name")
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        obj.score = obj.score


@admin.register(models.OnMovie)
class OnMovieAdmin(admin.ModelAdmin):

    search_fields = ('film__name',)
    list_per_page = 20


@admin.register(models.ComingMovie)
class ComingMovieAdmin(admin.ModelAdmin):

    search_fields = ('film__name',)
    list_per_page = 20


@admin.register(models.FilmComment)
class FilmCommentAdmin(admin.ModelAdmin):
    list_display = ('film', 'create_time', 'update_time')
    actions = [active_true, active_false]


@admin.register(models.FilmReview)
class FilmReviewAdmin(admin.ModelAdmin):

    actions = [active_true, active_false]



