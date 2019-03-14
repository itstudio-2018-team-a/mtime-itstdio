from django.db import models


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name=u"新闻标题")
    author_id = models.IntegerField(verbose_name=u"作者ID(内部ID)")
    public_time = models.DateTimeField(auto_now=True, verbose_name=u"发表时间")
    view_times = models.IntegerField(verbose_name=u"浏览次数")
    hotpoint = models.IntegerField(verbose_name=u"热度")


class NewsComments(models.Model):
    news_id = models.IntegerField(verbose_name=u"新闻ID")
    content = models.CharField(max_length=255, verbose_name=u"评论内容")
    author_id = models.IntegerField(verbose_name="作者ID(内部ID)")
    public_time = models.DateTimeField(auto_now=True, verbose_name='发布时间')
