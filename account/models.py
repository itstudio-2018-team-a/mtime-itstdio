from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):
    user_django = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=u"用户_django")
    user_id = models.CharField(unique=True, db_index=True, max_length=16, verbose_name=u"用户ID")
    nickname = models.CharField(max_length=20, verbose_name=u"昵称")
    head_image = models.URLField(verbose_name=u"头像URL")
    active = models.BooleanField(default=True, verbose_name="活动")

# class BanList(models.Model):
#     pass
