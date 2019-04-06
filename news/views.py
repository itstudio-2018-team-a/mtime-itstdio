from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
import json
import datetime
from django.utils import timezone
# Create your views here.
from . import models
from account import models as account_models


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


# 获取热点新闻  今日热点
def get_hotpot_list(request):
    if request.method == 'GET':

        # # 获取现在的时间 今日
        # now = timezone.now()
        #
        # # 状态 active == True
        # hot_news = models.News.objects.filter(active=True,
        #                                       create_time__year=now.year,
        #                                       create_time__month=now.month,
        #                                       create_time__day=now.day).order_by('-hits', '-create_time')[:10]

        hot_news = models.News.objects.filter(active=True).order_by('-hits', '-create_time')[:10]
        num = len(hot_news)
        content = {'num': num, 'list': [], 'status': 'success'}
        for one in hot_news:
            content['list'].append({
                'news_id': one.id,
                'title': one.title,
                'content': one.content,
                # create_time
                'pub_time': str(one.create_time.strftime('%Y-%m-%d %H:%M:%S')),
                'update_time': str(one.update_time.strftime('%Y-%m-%d %H:%M:%S')),
                'picture': one.picture.url,
            })

        return response_success(content)
    else:
        return HttpResponse(status=404)


# 获取全部新闻列表
def get_all_news(request):
    if request.method == 'GET':
        content = {'status': '', 'list': [], 'total_num': 0}

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

        all_news_list = models.News.objects.filter(active=True).order_by('-create_time')
        total_num = len(all_news_list)
        content['total_num'] = total_num

        paginator = Paginator(all_news_list, num)

        max_page_num = paginator.num_pages
        if page_num > max_page_num:
            page_num = max_page_num
        if page_num < 1:
            page_num = 1

        page_of_list = paginator.page(page_num).object_list
        content['on_page'] = page_num
        content['num_in_page'] = len(page_of_list)
        content['num'] = num
        content['max_page'] = max_page_num

        for one in page_of_list:
            content['list'].append({
                'news_id': one.id,
                'title': one.title,
                'content': one.content,

                'pub_time': str(one.create_time.strftime('%Y-%m-%d %H:%M:%S')),
                'update_time': str(one.update_time.strftime('%Y-%m-%d %H:%M:%S')),
                'picture': one.picture.url,
            })

        content['status'] = 'success'

        return response_success(content)
    else:
        HttpResponse(status=404)


# 获取特定新闻 参数id
def get_news(request):
    if request.method == 'GET':
        content = {'status': ''}

        try:
            news_id = int(request.GET.get('news_id'))
        except:
            news_id = 0
        if not news_id:
            content['status'] = 'news_error'
            return response_error(content)
        news = models.News.objects.filter(id=news_id, active=True)
        if not news:
            content['status'] = 'news_error'
            return response_error(content)
        news = news[0]

        content = {'title': news.title,
                   'body': news.content,
                   'news_id': news.id,
                   'pub_time': str(news.create_time.strftime('%Y-%m-%d %H:%M:%S')),
                   'update_time': str(news.update_time.strftime('%Y-%m-%d %H:%M:%S')),
                   'comment_num': news.commented_members,
                   'picture': news.picture.url,

                   'status': 'success',
                   }

        return response_success(content)
    else:
        return HttpResponse(status=404)


# 11
# 获取评论列表 特定新闻
def get_commit_list(request):
    if request.method == 'GET':
        content = {'status': '', 'list': [], 'total_num': 0}

        try:
            news_id = int(request.GET.get('news_id', default='0'))
        except :
            news_id = 0
        if not news_id:
            content['status'] = 'news_error'
            return response_error(content)
        news = models.News.objects.filter(id=news_id, active=True)
        if not news_id:
            content['status'] = 'news_error'
            return response_error(content)
        news = news[0]

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

        all_comments_list = models.NewsComment.objects.filter(news=news).order_by('-create_time')
        total_num = len(all_comments_list)
        content['total_num'] = total_num

        paginator = Paginator(all_comments_list, num)

        max_page_num = paginator.num_pages
        if page_num > max_page_num:
            page_num = max_page_num
        if page_num < 1:
            page_num = 1

        page_of_list = paginator.page(page_num).object_list
        content['on_page'] = page_num
        content['num_in_page'] = len(page_of_list)
        content['news_id'] = news_id
        content['num'] = num
        content['max_page'] = max_page_num

        for one in page_of_list:
            content['list'].append({
                'comment_id': one.id,
                'content': one.content,
                'author_id': one.author.id,
                'author_name': one.author.username,
                'author_head': one.author.head_image.url,
                'author_nickname': one.author.nickname,
                'time': str(one.create_time.strftime('%Y-%m-%d %H:%M:%S')),
            })

        content['status'] = 'success'

        return response_success(content)

    else:
        return HttpResponse(status=404)


# 进行评论
def commit_news(request):
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
            news_id = int(json_data['news_id'])
        except:
            news_id = 0
        if not news_id:
            content['status'] = 'news_error'
            return response_error(content)
        news = models.News.objects.filter(id=news_id, active=True)
        if not news:
            content['status'] = 'news_error'
            return response_error(content)
        news = news[0]

        comment = models.NewsComment.objects.filter(news=news, author=user)
        if comment:
            content['status'] = 'commented'
            return response_error(content)

        try:
            information = str(json_data['content'])
        except:
            information = ''
        if not information:
            content['status'] = 'content_error'
            return response_error(content)

        comment = models.NewsComment(author=user,
                                     news=news,
                                     content=information)
        comment.save()
        news.commented_members += 1
        news.save()

        content['status'] = 'success'

        return response_success(content)
    else:
        return HttpResponse(status=404)


def delete_comment(request):
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
            comment_id = json_data['comment_id']
        except:
            comment_id = 0
        if not comment_id:
            content['status'] = 'comment_error'
            return response_error(content)
        comment = models.NewsComment.objects.filter(id=comment_id, active=True)
        if not comment:
            content['status'] = 'comment_error'
            return response_error(content)
        comment = comment[0]

        if comment.author != user:
            content['status'] = 'deny'
            return response_error(content)

        comment.news.commented_members -= 1
        comment.news.save()
        comment.delete()
        content = {'status': 'success'}

        return response_success(content)
    else:
        return HttpResponse(status=404)











