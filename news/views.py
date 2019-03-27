from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
import json
# Create your views here.
from . import models


# 获取热点新闻
def get_hotpot_list(request):
    if request.method == 'GET':
        hot_news = models.News.objects.filter().order_by('-hits', '-create_time')

    else:
        HttpResponse(status=404)


# 获取全部新闻列表
def get_all_news(request):
    if request.method == 'GET':
        all_news_list = models.News.objects.all()

        # 分页器 每页 10 个新闻
        paginator = Paginator(all_news_list, 10)
        page_num = request.GET.get('page', default=1)

        max_page_num = paginator.count()
        if page_num > max_page_num:
            page_num = max_page_num
        if page_num < 1:
            page_num = 1

        page_of_list = paginator.page(page_num)

        content = {}
        content['list'] = page_of_list.object_list



        

    else:
        HttpResponse(status=404)


# 获取特定新闻 参数id
def get_news(request, news_id):
    if request.method == 'GET':
        pass
    else:
        HttpResponse(status=404)


# 进行评论
def commit_news(request):
    if request.method == 'POST':
        pass
    else:
        HttpResponse(status=404)


# 获取评论列表 特定新闻
def get_commit_list(request, news_id):
    if request.method == 'GET':
        pass
    else:
        HttpResponse(status=404)















