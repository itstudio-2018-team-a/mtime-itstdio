from django.contrib.auth.models import AbstractUser
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=16, verbose_name=u'用户名', unique=True, db_index=True)
    password = models.CharField(max_length=20, verbose_name=u'密码')
    nickname = models.CharField(max_length=20, verbose_name=u'昵称')
    head_image = models.ImageField(verbose_name=u'头像', upload_to='upload/%Y/%m')
    email = models.EmailField(verbose_name=u'邮箱')

    active = models.BooleanField(verbose_name=u'状态', default=False)

    class Meta:

        verbose_name = u'用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerificationCode(models.Model):
    email = models.EmailField(verbose_name=u'邮箱')
    code = models.CharField(max_length=10, verbose_name=u'验证码')

    # 判断是否 失效
    # 有效时间为 5 min
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'生成时间')

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email


class BlackList(models.Model):
    user = models.ForeignKey(User, verbose_name=u'用户', on_delete=models.PROTECT)
    reason = models.CharField(max_length=1024, verbose_name=u'原因')
    ip = models.CharField(max_length=20, verbose_name=u'IP地址', blank=True)
    mac = models.CharField(max_length=100, verbose_name=u'MAC地址', blank=True)
    banned_time = models.DateTimeField(auto_now_add=True, verbose_name=u'被禁时间')
    lasting_time = models.CharField(max_length=30, verbose_name=u'持续时间')

    class Meta:
        verbose_name = u'黑名单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username



