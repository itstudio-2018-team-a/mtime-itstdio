from django.db import models
from account import models as account_model
<<<<<<< HEAD


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name=u"新闻标题")
    author_id = models.IntegerField(verbose_name=u"作者ID(内部ID)")
    # content 内容以文件的形式保存
    public_time = models.DateTimeField(auto_now=True, verbose_name=u"发表时间")
    view_times = models.IntegerField(verbose_name=u"浏览次数")
    hotpoint = models.IntegerField(verbose_name=u"热度")
=======
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
>>>>>>> fix

    class Meta:
        verbose_name = u'新闻'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


<<<<<<< HEAD
class NewsComments(models.Model):
    news_id = models.IntegerField(verbose_name=u"新闻ID")
    content = models.CharField(max_length=255, verbose_name=u"评论内容")
    author_id = models.IntegerField(verbose_name="作者ID(内部ID)")
    public_time = models.DateTimeField(auto_now=True, verbose_name='发布时间')
=======
class NewsComment(models.Model):
    news = models.ForeignKey(News, verbose_name=u'新闻', on_delete=models.PROTECT)
    author = models.ForeignKey(account_model.User, verbose_name=u'作者', on_delete=models.PROTECT)
    content = models.CharField(max_length=1024, verbose_name=u'内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'评论时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')
    active = models.BooleanField(default=True, verbose_name=u'情况')
>>>>>>> fix

    class Meta:
        verbose_name = u'新闻评论'
        verbose_name_plural = verbose_name

    def __str__(self):
<<<<<<< HEAD
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
=======
        return u'%s %s' % (self.news.title, self.author.username)
>>>>>>> fix


