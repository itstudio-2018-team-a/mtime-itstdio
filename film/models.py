from django.db import models


class Film(models.Model):
    title = models.CharField(max_length=40, verbose_name=u'电影标题')
    info = models.CharField(max_length=1024, verbose_name=u'电影简介')
    public_time = models.DateTimeField(verbose_name=u'上映时间')
    score = models.IntegerField(default=-1, verbose_name=u'评分')
    marking_members = models.IntegerField(default=0, verbose_name=u'评分人数')
    poster = models.URLField(verbose_name=u'海报')
    commenting_members = models.IntegerField(default=0, verbose_name=u'评论数')


class OnMovie(models.Model):
    film_id = models.IntegerField(verbose_name=u'电影id')


class ComingMovie(models.Model):
    film_id = models.IntegerField(verbose_name=u'电影ID')
