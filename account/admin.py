from django.contrib import admin
from django.utils.html import format_html

from . import models
from . import forms


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):

    form = forms.RegisterForm

    list_display = ('image_data', 'username', 'email', 'nickname', 'active',)
    readonly_fields = ('image_data',)
    list_display_links = ('image_data', 'username',)
    list_per_page = 20
    search_fields = ('username', 'email', 'nickname')
    list_filter = ('active',)

    field = ('username', 'password', 'nickname', 'head_image', 'email', 'active',)

    def save_model(self, request, obj, form, change):
        obj.username = obj.username
        obj.password = obj.password
        obj.email = obj.email
        return super().save_model(request, obj, form, change)

    def image_data(self, obj):
        return format_html('<img src="{}" width="25px"/>', obj.head_image.url)
    image_data.short_description = u'头像'

    # action
    def active_false(self, request, queryset):
        number = queryset.update(active=False)
        return self.message_user(request, number)
    active_false.short_description = "禁用"

    def active_true(self, request, queryset):
        number = queryset.update(active=True)
        return self.message_user(request, number)
    active_true.short_description = "启用"

    actions = [active_true, active_false]


@admin.register(models.VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    form = forms.VerificationCodeForm
    list_display = ('email', 'code', 'create_time')
    list_per_page = 20
    search_fields = ('email',)
    ordering = ('-create_time',)
    field = ('email', 'code', 'create_time')

    def save_model(self, request, obj, form, change):
        obj.email = obj.email
        obj.code = obj.code

        return super().save_model(request, obj, form, change)


@admin.register(models.BlackList)
class BlackListAdmin(admin.ModelAdmin):
    list_display = ('user', 'reason', 'banned_time', 'lasting_time')
    list_per_page = 20
    search_fields = ('user__username',)


@admin.register(models.VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BlackList)
class BlackListAdmin(admin.ModelAdmin):
    pass







