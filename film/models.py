from django.db import models
from account import models as account_model
<<<<<<< HEAD


class Film(models.Model):
    title = models.CharField(max_length=40, verbose_name=u'电影标题')
    info = models.CharField(max_length=1024, verbose_name=u'电影简介')
    public_time = models.DateTimeField(verbose_name=u'上映时间')
    score = models.IntegerField(default=-1, verbose_name=u'评分')
    marking_members = models.IntegerField(default=0, verbose_name=u'评分人数')
    poster = models.URLField(verbose_name=u'海报')
    commenting_members = models.IntegerField(default=0, verbose_name=u'评论数')
=======
from ckeditor_uploader.fields import RichTextUploadingField


class Tags(models.Model):
    tag = models.CharField(max_length=10, verbose_name=u'标签', unique=True)

    class Meta:
        verbose_name = u'标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag


class Film(models.Model):
    name = models.CharField(max_length=40, verbose_name=u'电影名')
    info = models.CharField(max_length=1024, verbose_name=u'电影简介')
    on_time = models.DateTimeField(verbose_name=u'上映时间')
    tag = models.ManyToManyField(Tags, verbose_name=u'标签')

    # 页面上的 宽海报
    poster = models.ImageField(verbose_name=u'海报', upload_to='upload')
    # 电影的头像
    head_image = models.ImageField(verbose_name=u'电影封面', upload_to='upload')

    score = models.FloatField(default=0.0, verbose_name=u'评分')
    marked_members = models.IntegerField(default=0, verbose_name=u'评分人数')

    commented_member = models.IntegerField(default=0, verbose_name=u'评论人数')
    active = models.BooleanField(default=True, verbose_name=u'情况')
>>>>>>> fix

    class Meta:
        verbose_name = u'电影'
        verbose_name_plural = verbose_name

    def __str__(self):
<<<<<<< HEAD
        return self.title


class OnMovie(models.Model):
    film_id = models.IntegerField(verbose_name=u'电影ID')

    class Meta:
        verbose_name = u'上映电影'
        verbose_name_plural = verbose_name

    def __str__(self):
        film_title = Film.objects.filter(id=self.film_id)[0].title
        return film_title

    def get_film_title(self):
        film_title = Film.objects.filter(id=self.film_id)[0].title
        return film_title
    get_film_title.short_description = u'电影名'

    def get_film_public_time(self):
        film_public_time = Film.objects.filter(id=self.film_id)[0].public_time
        return film_public_time
    get_film_public_time.short_description = u'上映时间'
    get_film_public_time.admin_order_field = 'get_film_public_time'


class ComingMovie(models.Model):
    film_id = models.IntegerField(verbose_name=u'电影ID')
=======
        return self.name


class Mark(models.Model):
    user = models.ForeignKey(account_model.User, verbose_name=u'评分人', on_delete=models.PROTECT)
    film = models.ForeignKey(Film, verbose_name=u'评分电影', on_delete=models.PROTECT)
    score = models.IntegerField(blank=False, verbose_name=u'分值')

    class Meta:
        verbose_name = u'评分'
        verbose_name_plural = verbose_name

    def __str__(self):
        return u'%s %s %s' % (self.film.name, self.score, self.user.username)


class OnMovie(models.Model):
    film = models.ForeignKey(Film, verbose_name=u'上映电影', on_delete=models.PROTECT)

    class Meta:
        verbose_name = u'上映电影'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.film.name


class ComingMovie(models.Model):
    film = models.ForeignKey(Film, verbose_name=u'即将上映电影', on_delete=models.PROTECT)
>>>>>>> fix

    class Meta:
        verbose_name = u'即将上映电影'
        verbose_name_plural = verbose_name

    def __str__(self):
<<<<<<< HEAD
        film_title = Film.objects.filter(id=self.film_id)[0].title
        return film_title

    def get_film_title(self):
        film_title = Film.objects.filter(id=self.film_id)[0].title
        return film_title
    get_film_title.short_description = u'电影名'

    def get_film_public_time(self):
        film_public_time = Film.objects.filter(id=self.film_id)[0].public_time
        return film_public_time
    get_film_public_time.short_description = u'上映时间'
    get_film_public_time.admin_order_field = 'get_film_public_time'


class FilmComment(models.Model):
    film_id = models.IntegerField(db_index=True, verbose_name=u'电影ID')
    author_id = models.IntegerField(db_index=True, verbose_name=u'作者ID')
    content = models.CharField(max_length=1024, verbose_name=u'评论内容')

    class Meta:
        verbose_name = u'电影评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        film_title = Film.objects.filter(id=self.film_id)[0].title
        return film_title

    def get_film_title(self):
        film_title = Film.objects.filter(id=self.film_id)[0].title
        return film_title
    get_film_title.short_description = u'电影名'

    def get_author_name(self):
        author_name = account_model.MyUser.objects.filter(id=self.author_id)[0].username
        return author_name
    get_author_name.short_description = u'作者'


class FilmReview(models.Model):
    film_id = models.IntegerField(db_index=True, verbose_name=u'film_id')
    author_id = models.IntegerField(db_index=True, verbose_name=u'作者ID')
    # +++
    film_review_title = models.CharField(max_length=50, verbose_name=u'影评标题')
    # content = 内容存入文件
    image = models.URLField(null=True, verbose_name=u'缩略图URL')

    class Meta:
        verbose_name = u'影评'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.film_review_title

    def get_film_title(self):
        film_title = Film.objects.filter(id=self.film_id)[0].title
        return film_title
    get_film_title.short_description = u'电影名'

    def get_author_name(self):
        author_name = account_model.MyUser.objects.filter(id=self.author_id)[0].username
        return author_name
    get_author_name.short_description = u'作者'


class FilmReviewComment(models.Model):
    film_review_id = models.IntegerField(db_index=True, verbose_name=u'影评ID')
    author_id = models.IntegerField(db_index=True, verbose_name=u'作者ID')
    content = models.CharField(max_length=1024, verbose_name=u'评论内容')
=======
        return self.film.name


# 对电影的评论 短影评
class FilmComment(models.Model):
    film = models.ForeignKey(Film, verbose_name=u'电影', on_delete=models.PROTECT)
    author = models.ForeignKey(account_model.User, verbose_name=u'作者', on_delete=models.PROTECT)
    content = models.CharField(max_length=1024, verbose_name=u'评论内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'评论时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')
    active = models.BooleanField(default=True, verbose_name=u'情况')

    class Meta:
        verbose_name = u'短影评'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.film.name


# 电影的影评 长影评
class FilmReview(models.Model):
    film = models.ForeignKey(Film, verbose_name=u'电影', on_delete=models.PROTECT)
    author = models.ForeignKey(account_model.User, verbose_name=u'作者', on_delete=models.PROTECT)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'评论时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')
    title = models.CharField(max_length=50, verbose_name=u'标题')
    subtitle = models.CharField(max_length=50, verbose_name=u'副标题')
    content = RichTextUploadingField(verbose_name=u'内容')
    commented_members = models.IntegerField(default=0, verbose_name=u'评论人数')
    hits = models.IntegerField(default=0, verbose_name=u'点击量')

    thumbnail = models.ImageField(verbose_name=u'缩略图', upload_to='upload')

    active = models.BooleanField(default=True, verbose_name=u'情况')

    class Meta:
        verbose_name = u'长影评'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class FilmReviewComment(models.Model):
    film_review = models.ForeignKey(FilmReview, verbose_name=u'影评', on_delete=models.PROTECT)
    author = models.ForeignKey(account_model.User, verbose_name=u'作者', on_delete=models.PROTECT)
    content = models.CharField(max_length=1024, verbose_name=u'内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'评论时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')
    active = models.BooleanField(default=True, verbose_name=u'情况')
>>>>>>> fix

    class Meta:
        verbose_name = u'影评评论'
        verbose_name_plural = verbose_name

    def __str__(self):
<<<<<<< HEAD
        film_review_title = FilmReview.objects.filter(id=self.film_review_id)[0].film_review_title
        return film_review_title

    def get_film_review_title(self):
        film_review_title = FilmReview.objects.filter(id=self.film_review_id)[0].film_review_title
        return film_review_title
    get_film_review_title.short_description = u'影评标题'

    def get_author_name(self):
        author_name = account_model.MyUser.objects.filter(id=self.author_id)[0].username
        return author_name
    get_author_name.short_description = u'作者'

    def get_film_title(self):
        film_id = FilmReview.objects.filter(id=self.film_review_id)[0].film_id
        film_title = Film.objects.filter(id=film_id)[0].title
        return film_title
    get_film_title.short_description = u'电影名'
=======
        return u'%s %s' % (self.film_review.title, self.author.username)
>>>>>>> fix


