from django.db import models


class Film(models.Model):
    title = models.CharField(max_length=40, verbose_name=u'电影标题')
    info = models.CharField(max_length=255, verbose_name=u'电影简介')
    public_time = models.DateTimeField(verbose_name=u'上映时间')
    score = models.IntegerField(default=-1, verbose_name=u'评分')
    marking_members = models.IntegerField(default=0, verbose_name=u'评分人数')
    poster = models.URLField(verbose_name=u'海报')
    commenting_members = models.IntegerField(default=0, verbose_name=u'评论数')


class FilmComment(models.Model):
    film_id = models.IntegerField(db_index=True, verbose_name=u'电影ID')
    author_id = models.IntegerField(db_index=True, verbose_name=u'作者ID')
    content = models.CharField(max_length=1024, verbose_name=u'评论内容')


class FilmReview(models.Model):
    film_id = models.IntegerField(db_index=True, verbose_name=u'film_id')
    author_id = models.IntegerField(db_index=True, verbose_name=u'作者ID')
    # content = 内容存入文件
    image = models.URLField(null=True, verbose_name=u'缩略图URL')


class FilmReviewComment(models.Model):
    film_review_id = models.IntegerField(db_index=True, verbose_name=u'影评ID')
    author_id = models.IntegerField(db_index=True, verbose_name=u'作者ID')
    content = models.CharField(max_length=1024, verbose_name=u'评论内容')
