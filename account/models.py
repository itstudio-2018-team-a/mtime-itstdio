from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    email = models.EmailField(_('email address'),db_index=True,unique=True,verbose_name=u"电子邮件")
    nickname = models.CharField(max_length=20, verbose_name=u"昵称")
    head_image = models.URLField(verbose_name=u"头像URL")