from django.contrib import admin
from django.utils.html import format_html

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('image_data', 'username', 'email', 'nickname', 'active',)
    readonly_fields = ('image_data',)
    list_display_links = ('image_data', 'username',)
    list_per_page = 20
    search_fields = ('username', 'email', 'nickname')
    list_filter = ('active',)

    def image_data(self, obj):
        return format_html('<img src="{}" width="25px"/>', obj.head_image.url)
    image_data.short_description = u'头像'


@admin.register(models.VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BlackList)
class BlackListAdmin(admin.ModelAdmin):
    pass









