from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from . import models
import json
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
                'image': one.head_image,
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
        HttpResponse(status=404)


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
        HttpResponse(status=404)


