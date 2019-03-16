from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    nickname = models.CharField(max_length=20, verbose_name=u"昵称")
    head_image = models.URLField(verbose_name=u"头像URL")

    class Meta:
        indexes = [models.Index(['email', 'email']), models.Index(['username', 'username'])]
        unique_together = ('email',)
