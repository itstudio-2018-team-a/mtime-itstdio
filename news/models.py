from django.db import models
from account import models as account_model


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name=u"新闻标题")
    author_id = models.IntegerField(verbose_name=u"作者ID(内部ID)")
    # content 内容以文件的形式保存
    public_time = models.DateTimeField(auto_now=True, verbose_name=u"发表时间")
    view_times = models.IntegerField(verbose_name=u"浏览次数")
    hotpoint = models.IntegerField(verbose_name=u"热度")

    class Meta:
        verbose_name = u'新闻'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class NewsComments(models.Model):
    news_id = models.IntegerField(verbose_name=u"新闻ID")
    content = models.CharField(max_length=255, verbose_name=u"评论内容")
    author_id = models.IntegerField(verbose_name="作者ID(内部ID)")
    public_time = models.DateTimeField(auto_now=True, verbose_name='发布时间')

    class Meta:
        verbose_name = u'新闻评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        news_title = News.objects.filter(id=self.news_id)[0].title
        return news_title

    def get_news_title(self):
        news_title = News.objects.filter(id=self.news_id)[0].title
        return news_title
    get_news_title.short_description = u'新闻标题'

    def get_author_name(self):
        author_name = account_model.MyUser.objects.filter(id=self.author_id)[0].username
        return author_name
    get_author_name.short_description = u'作者'


