from django.db import models
from account import models as account_model
from ckeditor_uploader.fields import RichTextUploadingField


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'新闻标题')
    author = models.ForeignKey(account_model.User, verbose_name=u'作者', on_delete=models.PROTECT)
    content = RichTextUploadingField(verbose_name=u'内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')
    hits = models.IntegerField(default=0, verbose_name=u'点击量')
    active = models.BooleanField(default=True, verbose_name=u'情况')

    commented_members = models.IntegerField(default=0, verbose_name=u'评论人数')
    picture = models.ImageField(verbose_name=u'图片', upload_to='upload')

    class Meta:
        verbose_name = u'新闻'
        verbose_name_plural = verbose_name

        ordering = ['-create_time']

    def __str__(self):
        return self.title


class NewsComment(models.Model):
    news = models.ForeignKey(News, verbose_name=u'新闻', on_delete=models.PROTECT)
    author = models.ForeignKey(account_model.User, verbose_name=u'作者', on_delete=models.PROTECT)
    content = models.CharField(max_length=1024, verbose_name=u'内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'评论时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')
    active = models.BooleanField(default=True, verbose_name=u'情况')

    class Meta:
        verbose_name = u'新闻评论'
        verbose_name_plural = verbose_name

        ordering = ['create_time']

    def __str__(self):
        return u'%s %s' % (self.news.title, self.author.username)



