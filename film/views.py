from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from . import models
import json
from django.utils import timezone
# Create your views here.


# {
#   "num":"数量(int)",
#   "list":[{
#     "title":"电影标题",
#     "image":"缩略图",
#     "info":"简介",
#     "time":"YYYY-MM-DD hh:mm:ss",
#     "film_id":"电影ID"
#     }],
#     "status": "ok"
# }
# status存在以下几种情况
#     ok:正常
#     deny：拒绝
#     null：电影列表为空
#     error：未知错误

# 11
# 获取全部电影
def get_film_list(request):
    if request.method == 'GET':
        all_film_list = models.Film.objects.filter(active=True).order_by('-on_time')

        num = int(request.GET.get('num', default='10'))
        paginator = Paginator(all_film_list, num)

        page_num = int(request.GET.get('page', default='1'))

        max_page_num = paginator.count
        if page_num > max_page_num:
            page_num = max_page_num
        if page_num < 1:
            page_num = 1

        page_of_list = paginator.page(page_num)
        total_num = len(all_film_list)
        content = {'list': [], 'num': num, 'page_num': page_num, 'total_num': total_num, 'status': 'ok'}

        for one in page_of_list.object_list:
            content['list'].append({
                'title': one.name,
                'image': one.head_image.url,
                'info': one.info,
                'film_id': one.id,
                'time': str(one.on_time.strftime('%Y-%m-%d %H:%M:%S'))
            })

        content = json.dumps(content)

        return HttpResponse(content,
                            content_type='application/json;charset = utf-8',
                            status='200',
                            reason='success',
                            charset='utf-8')

    else:
        return HttpResponse(status=404)


# {
# #   "title" : "标题",
# #   "image" :"图片",
# #   "info" : "介绍",
# #   "relase_date": "YYYY-MM-DD",
# #   "time" : "hh:mm:ss",
# #   "film_id" : "电影id",
# #   "mark": "评分",
# #   "status" : "ok"
# # }
# # status存在以下几种可能
# #     ok：正常
# #     unknown:未知电影
# #     error：未知错误

# 11
# 获取特定电影 参数id
def get_film(request):
    if request.method == 'GET':
        film_id = request.GET.get('film_id') # 000
        the_film = models.Film.objects.filter(id=film_id, active=True)

        if the_film:
            the_film = the_film[0]

            content = {'title': the_film.name,
                       'image': the_film.head_image.url,
                       'film_id': the_film.id,
                       'mark': the_film.score,
                       'relase_date': str(the_film.on_time.strftime('%Y-%m-%d')),
                       'time': str(the_film.on_time.strftime('%H:%M:%S')),
                       'marked_members': the_film.marked_members,
                       'comment_members': the_film.commented_member,
                       'status': 'ok',
                       }

            content = json.dumps(content)

            return HttpResponse(content,
                                content_type='application/json;charset = utf-8',
                                status='200',
                                reason='success',
                                charset='utf-8')
        else:
            # 返回错误信息
            # 找不到指定新闻 status
            content = {'status': 'unknown'}

            content = json.dumps(content)

            return HttpResponse(content,
                                content_type='application/json;charset = utf-8',
                                status='404',
                                reason='Not_Found',
                                charset='utf-8')

    else:
        return HttpResponse(status=404)


def get_on_movie(request):
    if request.method == 'GET':
        on_movies = models.OnMovie.objects.all()

        num = len(on_movies)
        content = {'num': num, 'list': [], 'status': 'ok'}
        for one in on_movies:
            content['list'].append({
                'title': one.film.name,
                'film_id': one.film.id,
                'image': one.film.head_image.url,
                'info': one.film.info,
                'release_date': str(one.film.on_time.strftime('%H:%M:%S')),
                'mark': one.film.score,
                'marked_members': one.film.marked_members,
                'commented_members': one.film.commented_member,
            })

        content = json.dumps(content)

        return HttpResponse(content,
                            content_type='application/json;charset = utf-8',
                            status='200',
                            reason='success',
                            charset='utf-8')
    else:
        return HttpResponse(status=404)


def get_coming_movie(request):
    if request.method == 'GET':
        on_movies = models.ComingMovie.objects.all()

        num = len(on_movies)
        content = {'num': num, 'list': [], 'status': 'ok'}
        for one in on_movies:
            content['list'].append({
                'title': one.film.name,
                'film_id': one.film.id,
                'image': one.film.head_image.url,
                'info': one.film.info,
                'release_date': str(one.film.on_time.strftime('%H:%M:%S')),
                'mark': one.film.score,
                'marked_members': one.film.marked_members,
                'commented_members': one.film.commented_member,
            })

        content = json.dumps(content)

        return HttpResponse(content,
                            content_type='application/json;charset = utf-8',
                            status='200',
                            reason='success',
                            charset='utf-8')
    else:
        return HttpResponse(status=404)


def get_film_review_list(request):
    if request.method == 'GET':
        all_review_list = models.FilmReview.objects.filter(active=True).order_by('-create_time')

        num = int(request.GET.get('num', default=10))
        paginator = Paginator(all_review_list, num)

        page_num = int(request.GET.get('page', default='1'))

        max_page_num = paginator.count
        if page_num > max_page_num:
            page_num = max_page_num
        if page_num < 1:
            page_num = 1

        page_of_list = paginator.page(page_num)
        total_num = len(all_review_list)
        content = {'list': [], 'total_num': total_num, 'num': num, 'status': 'ok'}

        for one in page_of_list.object_list:
            content['list'].append({
                'film_id': one.film.id,
                'author_name': one.author.username,
                'author_id': one.author.id,
                'author_head': one.author.head_image.url,
                'title': one.title,
                'subtitle': one.subtitle,
                'content': one.content,
                'comment_members': one.commented_members,
                'thumbnail': one.thumbnail.url,
                'pub_time': str(one.create_time.strftime('%Y-%m-%d %H:%M:%S')),

            })

            content = json.dumps(content)

            return HttpResponse(content,
                                content_type='application/json;charset = utf-8',
                                status='200',
                                reason='success',
                                charset='utf-8')
    else:
        return HttpResponse(status=404)


def get_hot_review(request):
    if request.method == 'GET':

        hot_review = models.FilmReview.objects.filter(active=True).order_by('-hits', '-create_time')[:10]

        content = {'num': hot_review.count(), 'list': [], 'status': 'ok'}
        for one in hot_review:
            content['list'].append({
                'comment_id': one.id,
                'title': one.title,
                'subtitle': one.subtitle,
                'author_id': one.author.id,
                'author_name': one.author.username,
                'author_head': one.author.head_image.url,
                'comment_num': one.commented_members,
                'create_time': str(one.create_time.strftime('%Y-%m-%d %H:%M:%S')),
                'update_time': str(one.update_time.strftime('%Y-%m-%d %H:%M:%S')),

            })

        content = json.dumps(content)

        return HttpResponse(content,
                            content_type='application/json;charset = utf-8',
                            status='200',
                            reason='success',
                            charset='utf-8')

    else:
        return HttpResponse(status=404)


def get_review(request):
    if request.method == 'GET':
        review_id = request.GET.get('review_id') # 000
        the_review = models.FilmReview.objects.filter(id=review_id, active=True)

        if the_review:
            the_review = the_review[0]

            content = {
                'title': the_review.title,
                'subtitle': the_review.subtitle,
                'author_id': the_review.author.id,
                'author_name': the_review.author.username,
                'author_head': the_review.author.head_image.url,
                'comment_num': the_review.commented_members,
                'create_time': str(the_review.create_time.strftime('%Y-%m-%d %H:%M:%S')),
                'update_time': str(the_review.update_time.strftime('%Y-%m-%d %H:%M:%S')),
                'body': the_review.content,

                'status': 'ok',
                }

            content = json.dumps(content)

            return HttpResponse(content,
                                content_type='application/json;charset = utf-8',
                                status='200',
                                reason='success',
                                charset='utf-8')

        else:

            content = {'status': 'unknow'}

            content = json.dumps(content)

            return HttpResponse(content,
                                content_type='application/json;charset = utf-8',
                                status='404',
                                reason='Not_Found',
                                charset='utf-8')
    else:
        return HttpResponse(status=404)


def get_short_comment(request):
    if request.method == 'GET':
        film_id = request.GET.get('film_id')

        content = {'list': []}

        if film_id:
            film = models.Film.objects.filter(id=film_id, active=True)
            if film:
                film = film[0]
                all_comments_list = models.FilmComment.objects.filter(film=film, active=True).order_by('-create_time')
                total_num = len(all_comments_list)
                content['total_num'] = total_num
                num = request.GET.get('num', default=10)
                paginator = Paginator(all_comments_list, num)
                content['num'] = num

                page_num = int(request.GET.get('page', default='1'))

                max_page_num = paginator.count
                if page_num > max_page_num:
                    page_num = max_page_num
                if page_num < 1:
                    page_num = 1

                page_of_list = paginator.page(page_num).object_list
                for one in page_of_list:
                    content['list'].append({
                        'comment_id': one.id,
                        'content': one.content,
                        'nickname': one.author.nickname,
                        'user_id': one.author.id,
                        'time': str(one.create_time.strftime('%Y-%m-%d %H:%M:%S'))
                    })
                content['status'] = 'ok'

                content = json.dumps(content)

                return HttpResponse(content,
                                    content_type='application/json;charset = utf-8',
                                    status='200',
                                    reason='success',
                                    charset='utf-8')

        else:
            content['num'] = 0
            content['status'] = 'error'

            content = json.dumps(content)

            return HttpResponse(content,
                                content_type='application/json;charset = utf-8',
                                status='404',
                                reason='Not_Found',
                                charset='utf-8')
    else:
        return HttpResponse(status=404)


def get_review_comment(request):
    if request.method == 'GET':
        review_id = request.GET.get('review_id')
        content = {'list': []}
        if review_id:
            review = models.FilmReview.objects.filter(id=review_id, active=True)
            if review:
                review = review[0]
                all_comments_list = models.FilmReviewComment.objects.filter(film_review=review, active=True)

                total_num = len(all_comments_list)
                content['total_num'] = total_num
                num = int(request.GET.get('num', default='10'))
                paginator = Paginator(all_comments_list, num)
                content['num'] = num

                page_num = int(request.GET.get('page', default='1'))

                max_page_num = paginator.count
                if page_num > max_page_num:
                    page_num = max_page_num
                if page_num < 1:
                    page_num = 1

                page_of_list = paginator.page(page_num).object_list

                for one in page_of_list:
                    content['list'].append({
                        'comment_id': one.id,
                        'content': one.content,
                        'nickname': one.author.nickname,
                        'user_id': one.author.id,
                        'time': str(one.create_time.strftime('%Y-%m-%d %H:%M:%S'))
                    })

        content['num'] = 0
        content['status'] = 'unknown'
        content = json.dumps(content)

        return HttpResponse(content,
                            content_type='application/json;charset = utf-8',
                            status='404',
                            reason='Not_Found',
                            charset='utf-8')
    else:
        return HttpResponse(status=404)


def get_score(request):
    if request.method == 'GET':
        film_id = request.GET.get('film_id')
        if film_id:
            pass
        else:
            pass
    else:
        return HttpResponse(status=404)



