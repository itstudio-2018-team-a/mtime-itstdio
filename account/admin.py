from django.contrib import admin

from . import models


@admin.register(models.MyUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'nickname')
    list_per_page = 20
    search_fields = ('username', 'nickname')
    actions_on_top = True
    ordering = ('id',)

