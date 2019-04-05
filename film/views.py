from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from account import models as account_models
from . import models
import json
from django.utils import timezone
# Create your views here.


def response_success(content):
    content = json.dumps(content)
    return HttpResponse(content,
                        content_type='application/json;charset = utf-8',
                        status='200',
                        reason='OK',
                        charset='utf-8')


def response_error(content):
    content = json.dumps(content)
    return HttpResponse(content,
                        content_type='application/json;charset = utf-8',
                        status='400',
                        reason='Bad Request',
                        charset='utf-8')


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
        content = {'status': ''}

        try:
            num = int(request.GET.get('num', default='10'))
        except:
            content['status'] = 'num_error'
            return response_error(content)

        try:
            page_num = int(request.GET.get('page', default='1'))
        except:
            content['status'] = 'page_error'
            return response_error(content)

        all_film_list = models.Film.objects.filter(active=True).order_by('-on_time')
        paginator = Paginator(all_film_list, num)

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

        return response_success(content)

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
                       'info': the_film.info,
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


def get_on_four_movies_simple(request):
    if request.method == 'GET':
        on_movies = models.OnMovie.objects.all().order_by('-film__on_time')[:4]

        num = len(on_movies)

        content = {'num': num, 'list': [], 'status': 'ok'}

        for one in on_movies:
            content['list'].append({
                'pub_time': str(one.film.on_time.strftime('%m-%d')),
                'film_name': one.film.name,
                'info': one.film.info,
                'picture': one.film.head_image.url,
            })

        content = json.dumps(content)

        return HttpResponse(content,
                            content_type='application/json;charset = utf-8',
                            status='200',
                            reason='success',
                            charset='utf-8')
    else:
        return HttpResponse(status=404)


def get_on_four_movies_detailed(request):
    if request.method == 'GET':
        on_movies = models.OnMovie.objects.all().order_by('-film__on_time')[:4]

        num = len(on_movies)

        content = {'num': num, 'list': [], 'status': 'ok'}

        for one in on_movies:
            content['list'].append({
                'pub_time': str(one.film.on_time.strftime('%m-%d')),
                'film_name': one.film.name,
                'info': one.film.info,
                'picture': one.film.head_image.url,
            })

        content = json.dumps(content)

        return HttpResponse(content,
                            content_type='application/json;charset = utf-8',
                            status='200',
                            reason='success',
                            charset='utf-8')
    else:
        return HttpResponse(status=404)


def get_on_movie_list(request):
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
        on_movies = models.ComingMovie.objects.filter(film__active=True)

        num = len(on_movies)
        content = {'num': num, 'list': [], 'status': 'success'}

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

        return response_success(content)
    else:
        return HttpResponse(status=404)


def get_film_review_list(request):
    if request.method == 'GET':
        content = {'list': [], 'status': '', 'total_num': 0}

        try:
            num = int(request.GET.get('num', default='10'))
        except:
            num = 0
        if not num:
            content['status'] = 'num_error'
            return response_error(content)
        content['num'] = num

        try:
            page_num = int(request.GET.get('page', default='1'))
        except:
            page_num = -1
        if page_num == -1:
            content['status'] = 'page_error'
            return response_error(content)

        all_review_list = models.FilmReview.objects.filter(active=True).order_by('-create_time')
        total_num = len(all_review_list)
        content['total_num'] = total_num

        paginator = Paginator(all_review_list, num)

        max_page_num = paginator.count
        if page_num > max_page_num:
            page_num = max_page_num
        if page_num < 1:
            page_num = 1

        page_of_list = paginator.page(page_num).object_list
        content['on_page'] = page_num
        content['num_in_page'] = len(page_of_list)
        content['num'] = num

        for one in page_of_list:
            content['list'].append({
                'author_id': one.author.id,
                'author_name': one.author.username,
                'author_head': one.author.head_image.url,
                'author_nickname': one.author.nickname,

                'review_id': one.id,
                'title': one.title,
                'subtitle': one.subtitle,
                'thumbnail': one.thumbnail.url,
                'body': one.content,

                'create_time': str(one.create_time.strftime('%Y-%m-%d %H:%M:%S')),
                'update_time': str(one.update_time.strftime('%Y-%m-%d %H:%M:%S')),
                'comment_num': one.commented_members,

                'film_id': one.film.id,
                'film_name': one.film.name,
            })

            content['status'] = 'success'

            return response_success(content)
    else:
        return HttpResponse(status=404)


def get_hot_review(request):
    if request.method == 'GET':
        content = {'list': [], 'status': 'success'}

        hot_review = models.FilmReview.objects.filter(active=True).order_by('-hits', '-create_time')[:10]
        content['total_num'] = len(hot_review)

        for one in hot_review:
            content['list'].append({
                'author_id': one.author.id,
                'author_name': one.author.username,
                'author_head': one.author.head_image.url,
                'author_nickname': one.author.nickname,

                'review_id': one.id,
                'title': one.title,
                'subtitle': one.subtitle,
                'thumbnail': one.thumbnail.url,
                'body': one.content,

                'create_time': str(one.create_time.strftime('%Y-%m-%d %H:%M:%S')),
                'update_time': str(one.update_time.strftime('%Y-%m-%d %H:%M:%S')),
                'comment_num': one.commented_members,

                'film_id': one.film.id,
                'film_name': one.film.name,
            })

        return response_success(content)
    else:
        return HttpResponse(status=404)


def get_review(request):
    if request.method == 'GET':
        content = {'status': ''}

        try:
            review_id = int(request.GET.get('review_id'))
        except:
            review_id = 0
        if not review_id:
            content['status'] = 'review_error'
            return response_error(content)
        review = models.FilmReview.objects.filter(id=review_id, active=True)
        if not review:
            content['status'] = 'review_error'
            return response_error(content)
        review = review[0]

        content = {
            'author_id': review.author.id,
            'author_name': review.author.username,
            'author_head': review.author.head_image.url,
            'author_nickname': review.author.nickname,

            'review_id': review.id,
            'title': review.title,
            'subtitle': review.subtitle,
            'thumbnail': review.thumbnail.url,
            'body': review.content,

            'create_time': str(review.create_time.strftime('%Y-%m-%d %H:%M:%S')),
            'update_time': str(review.update_time.strftime('%Y-%m-%d %H:%M:%S')),
            'comment_num': review.commented_members,

            'film_id': review.film.id,
            'film_name': review.film.name,

            'status': 'success',
            }

        return response_success(content)
    else:
        return HttpResponse(status=404)


def get_short_comment(request):
    if request.method == 'GET':
        content = {'status': '', 'list': [], 'total_num': 0}

        try:
            film_id = int(request.GET.get('film_id'))
        except:
            film_id = 0
        if not film_id:
            content['status'] = 'film_error'
            return response_error(content)
        film = models.Film.objects.filter(id=film_id, active=True)
        if not film:
            content['status'] = 'film_error'
            return response_error(content)
        film = film[0]

        try:
            num = int(request.GET.get('num', default='10'))
        except:
            num = -1
        if num == -1:
            content['status'] = 'num_error'
            return response_error(content)
        content['num'] = num

        try:
            page_num = int(request.GET.get('page', default='1'))
        except:
            page_num = -1
        if page_num == -1:
            content['status'] = 'page_error'
            return response_error(content)

        all_comments_list = models.FilmComment.objects.filter(film=film, active=True).order_by('-create_time')
        total_num = len(all_comments_list)
        content['total_num'] = total_num

        paginator = Paginator(all_comments_list, num)

        max_page_num = paginator.count
        if page_num > max_page_num:
            page_num = max_page_num
        if page_num < 1:
            page_num = 1

        page_of_list = paginator.page(page_num).object_list
        content['on_page'] = page_num
        content['num_in_page'] = len(page_of_list)
        content['fim_id'] = film_id
        content['num'] = num

        for one in page_of_list:
            content['list'].append({
                'author_name': one.author.nickname,
                'author_nickname': one.author.nickname,
                'author_head': one.author.head_image.url,
                'author_id': one.author.id,

                'comment_id': one.id,
                'content': one.content,
                'time': str(one.create_time.strftime('%Y-%m-%d %H:%M:%S'))
            })

        content['status'] = 'success'

        return response_success(content)
    else:
        return HttpResponse(status=404)


def get_review_comment(request):
    if request.method == 'GET':
        content = {'status': '', 'list': [], 'total_num': 0}

        try:
            review_id = int(request.GET.get('review_id'))
        except:
            review_id = 0
        if not review_id:
            content['status'] = 'review_error'
            return response_error(content)
        review = models.FilmReview.objects.filter(id=review_id, active=True)
        if not review:
            content['status'] = 'review_error'
            return response_error(content)
        review = review[0]

        try:
            num = int(request.GET.get('num', default='10'))
        except:
            num = -1
        if num == -1:
            content['status'] = 'num_error'
            return response_error(content)
        content['num'] = num

        try:
            page_num = int(request.GET.get('page', default='1'))
        except:
            page_num = -1
        if page_num == -1:
            content['status'] = 'page_error'
            return response_error(content)

        all_comments_list = models.FilmReviewComment.objects.filter(film_review=review, active=True)
        total_num = len(all_comments_list)
        content['total_num'] = total_num

        paginator = Paginator(all_comments_list, num)

        max_page_num = paginator.count
        if page_num > max_page_num:
            page_num = max_page_num
        if page_num < 1:
            page_num = 1

        page_of_list = paginator.page(page_num).object_list
        content['on_page'] = page_num
        content['num_in_page'] = len(page_of_list)
        content['review_id'] = review_id
        content['num'] = num
        for one in page_of_list:
            content['list'].append({
                'author_name': one.author.nickname,
                'author_nickname': one.author.nickname,
                'author_head': one.author.head_image.url,
                'author_id': one.author.id,

                'comment_id': one.id,
                'content': one.content,
                'time': str(one.create_time.strftime('%Y-%m-%d %H:%M:%S'))
            })

        content['status'] = 'success'

        return response_success(content)

    else:
        return HttpResponse(status=404)


def write_short_comment(request):
    if request.method == 'POST':
        content = {'status': ''}

        try:
            user_id = int(request.session['user_id'])
        except:
            user_id = 0
        if not user_id:
            content['status'] = 'user_error'
            return response_error(content)
        user = account_models.User.objects.filter(id=user_id)
        if not user:
            content['status'] = 'user_error'
            return response_error(content)
        user = user[0]

        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            json_data = {}
        except Exception:
            json_data = {}
        if not json_data:
            content['status'] = 'json_error'
            return response_error(content)

        try:
            film_id = int(json_data['film_id'])
        except:
            film_id = 0
        if not film_id:
            content['status'] = 'film_error'
            return response_error(content)
        film = models.Film.objects.filter()
        if not film:
            content['status'] = 'film_error'
            return response_error(content)
        film = film[0]

        try:
            information = json_data['content']
        except:
            information = ''
        if not information:
            content['status'] = 'content_error'
            return response_error(content)

        comment = models.FilmComment(film=film,
                                     author=user,
                                     content=information,
                                     active=True)
        comment.save()
        content['status'] = 'success'

        return response_success(content)
    else:
        return HttpResponse(status=404)


def delete_short_comment(request):
    if request.method == 'POST':
        content = {'status': ''}

        try:
            user_id = int(request.session['user_id'])
        except:
            user_id = 0
        if not user_id:
            content['status'] = 'user_error'
            return response_error(content)
        user = account_models.User.objects.filter(id=user_id)
        if not user:
            content['status'] = 'user_error'
            return response_error(content)
        user = user[0]

        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            json_data = {}
        except Exception:
            json_data = {}
        if not json_data:
            content['status'] = 'json_error'
            return response_error(content)

        try:
            comment_id = int(json_data['comment_id'])
        except:
            comment_id = 0
        if not comment_id:
            content['status'] = 'comment_error'
            return response_error(content)
        comment = models.FilmComment.objects.filter(id=comment_id)
        if not comment_id:
            content['status'] = 'comment_error'
            return response_error(content)
        comment = comment[0]

        if comment.author != user:
            content['status'] = 'deny'
            return response_error(content)

        comment.delete()
        content = {'status': 'success'}

        return response_success(content)
    else:
        return HttpResponse(status=404)


def write_review(request):
    if request.method == 'POST':
        content = {'status': ''}

        try:
            user_id = int(request.session['user_id'])
        except:
            user_id = 0
        if not user_id:
            content['status'] = 'user_error'
            return response_error(content)
        user = account_models.User.objects.filter(id=user_id)
        if not user:
            content['status'] = 'user_error'
            return response_error(content)
        user = user[0]

        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            json_data = {}
        except Exception:
            json_data = {}
        if not json_data:
            content['status'] = 'json_error'
            return response_error(content)

        try:
            film_id = int(json_data['film_id'])
        except:
            film_id = 0
        if not film_id:
            content['status'] = 'film_error'
            return response_error(content)
        film = models.Film.objects.filter()
        if not film:
            content['status'] = 'film_error'
            return response_error(content)
        film = film[0]

        try:
            review_content = json_data['content']
            title = json_data['title']
            subtitle = json_data['subtitle']
        except:
            review_content = ''
            title = ''
            subtitle = ''
        if not (review_content and title and subtitle):
            content['status'] = 'lack_error'
            return response_error(content)

        try:
            img = request.FILES.get('thumbnail')
        except:
            img = 0
        if not img:
            content['status'] = 'thumbnail_error'
            return response_error(content)

        review = models.FilmReview(film=film,
                                   author=user,
                                   title=title,
                                   subtitle=subtitle,
                                   content=content,
                                   thumbnail=img,
                                   active=True)
        review.save()
        content['status'] = 'success'

        return response_success(content)
    else:
        return HttpResponse(status=404)


def delete_review(request):
    if request.method == 'POST':
        content = {'status': ''}

        try:
            user_id = int(request.session['user_id'])
        except:
            user_id = 0
        if not user_id:
            content['status'] = 'user_error'
            return response_error(content)
        user = account_models.User.objects.filter(id=user_id)
        if not user:
            content['status'] = 'user_error'
            return response_error(content)
        user = user[0]

        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            json_data = {}
        except Exception:
            json_data = {}
        if not json_data:
            content['status'] = 'json_error'
            return response_error(content)

        try:
            review_id = int(json_data['review_id'])
        except:
            review_id = 0
        if not review_id:
            content['status'] = 'review_error'
            return response_error(content)
        review = models.FilmReview.objects.filter(id=review_id, active=True)
        if not review:
            content['status'] = 'review_error'
            return response_error(content)
        review = review[0]

        if review.author != user:
            content['status'] = 'deny'
            return response_error(content)

        review.delete()
        content = {'status': 'success'}

        return response_success(content)
    else:
        return HttpResponse(status=404)


def search(request):
    if request.method == 'POST':
        content = {'status': ''}

        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            json_data = {}
        except Exception:
            json_data = {}
        if not json_data:
            content['status'] = 'json_error'
            return response_error(content)

        try:
            page_num = int(json_data['page'])
        except:
            page_num = 1
        try:
            num = int(json_data['name'])
        except:
            num = 10
        content['page'] = page_num
        content['num'] = num

        try:
            information = str(json_data['content'])
        except:
            information = ''
        if not information:
            content['status'] = 'content_error'
            return response_error(content)

        films_list = models.Film.objects.filter(name__icontains=information)

        total_num = len(films_list)
        content['list'] = []
        content['total_num'] = total_num

        if films_list:

            paginator = Paginator(films_list, num)

            max_page_num = paginator.count
            if page_num > max_page_num:
                page_num = max_page_num
            if page_num < 1:
                page_num = 1

            page_of_list = paginator.page(page_num)

            for one in page_of_list.object_list:
                content['list'].append({
                    'film_id': one.id,
                    'film_name': one.name,
                })

        content['status'] = 'success'
        return response_success(content)

    else:
        return HttpResponse(status=404)


def mark(request):
    if request.method == 'POST':
        content = {'status': ''}

        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            json_data = {}
        except Exception:
            json_data = {}
        if not json_data:
            content['status'] = 'json_error'
            return response_error(content)

        try:
            user_id = int(request.session['user_id'])
        except:
            user_id = 0
        if not user_id:
            content['status'] = 'user_error'
            return response_error(content)
        user = account_models.User.objects.filter(id=user_id)
        if not user:
            content['status'] = 'user_error'
            return response_error(content)
        user = user[0]

        try:
            film_id = int(json_data['film_id'])
        except:
            film_id = 0
        if not film_id:
            content['status'] = 'film_error'
        film = models.Film.objects.filter(id=film_id, active=True)
        if not film:
            content['status'] = 'film_error'
            return response_error(content)
        film = film[0]

        try:
            score = int(json_data['score'])
        except:
            score = -1
        if score < 0 or score > 10:
            score = -1
        if score == -1:
            content['status'] = 'score_error'
            return response_error(content)

        if models.Mark.objects.filter(user=user, film=film):
            content['status'] = 'marked'
            return response_error(content)

        film.score = (film.score * film.marked_members + score) / (film.marked_members + 1)
        film.marked_members += 1
        film.save()

        the_mark = models.Mark(user=user,
                               film=film,
                               score=score)
        the_mark.save()

        content['status'] = 'success'

        return response_success(content)
    else:
        return HttpResponse(status=404)


def mark_authority(request):
    if request.method == 'GET':
        content = {'status': ''}

        try:
            user_id = int(request.session['user_id'])
        except:
            user_id = 0
        if not user_id:
            content['status'] = 'un_login'
            return response_error(content)
        user = account_models.User.objects.filter(id=user_id)
        if not user:
            content['status'] = 'un_login'
            return response_error(content)
        user = user[0]

        try:
            film_id = int(request.GET.get('film_id'))
        except:
            film_id = 0
        if not film_id:
            content['status'] = 'film_error'
            return response_error(content)
        film = models.Film.objects.filter(id=film_id, active=True)
        if not film:
            content['status'] = 'film_error'
            return response_error(content)
        film = film[0]

        the_mark = models.Mark.objects.filter(user=user, film=film)
        if the_mark:
            content['status'] = 'marked'
            content['username'] = user.username
            content['score'] = the_mark.score
            return response_success(content)
        else:
            content['status'] = 'ready'
            return response_success(content)
    else:
        return HttpResponse(status=404)





