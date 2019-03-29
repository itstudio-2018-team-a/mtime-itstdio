from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
import json
import datetime
from django.utils import timezone
# Create your views here.
from . import models
from account import models as account_models

# {
#   "num": "新闻数量(int)",
#   "list":[{
#       "title": "文章标题",
#       "picture": "缩略图url",
#       "pub_time": "YYYY-MM-DD hh:mm:ss",
#       "new_id": "新闻id(int)"
#   }],
#   "status": "ok"
# }
# status存在几种可能情况
# ok；成功
# error：出错
#     此时可能不存在num和list元素


# 11
# 获取热点新闻  今日热点
def get_hotpot_list(request):
    if request.method == 'GET':
        # 获取现在的时间 今日
        now = timezone.now()

        # 状态 active == True
        hot_news = models.News.objects.filter(active=True,
                                              create_time__year=now.year,
                                              create_time__month=now.month,
                                              create_time__day=now.day).order_by('-hits', '-create_time')[:10]
        num = len(hot_news)
        content = {'num': num, 'list': [], 'status': 'ok'}
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
        print(content)

        content = json.dumps(content)

        return HttpResponse(content,
                            content_type='application/json;charset = utf-8',
                            status='200',
                            reason='success',
                            charset='utf-8')
    else:
        return HttpResponse(status=404)


# 11
# 获取全部新闻列表
def get_all_news(request):
    if request.method == 'GET':
        all_news_list = models.News.objects.filter(active=True).order_by('-create_time')

        # 分页器 每页 10 个新闻(default=10)
        num = int(request.GET.get('num', default='10'))
        paginator = Paginator(all_news_list, num)

        page_num = int(request.GET.get('page', default='1'))

        max_page_num = paginator.count
        if page_num > max_page_num:
            page_num = max_page_num
        if page_num < 1:
            page_num = 1

        page_of_list = paginator.page(page_num)
        total_num = len(all_news_list)
        content = {'list': [], 'total_num': total_num, 'num': num, 'status': 'ok'}

        for one in page_of_list.object_list:
            content['list'].append({
                'news_id': one.id,
                'title': one.title,
                'content': one.content,
                # create_time
                'pub_time': str(one.create_time.strftime('%Y-%m-%d %H:%M:%S')),
                'update_time': str(one.update_time.strftime('%Y-%m-%d %H:%M:%S')),
                'picture': one.picture.url,
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
#   "title": "新闻标题",
#   "body":"新闻内容(html)",
#   "pub_time": "YYYY-MM-DD hh:mm:ss",
#   "comment_num":"评论数量",
#   "status": "ok"
# }
#
#          status可能存在以下几种情况
# #             ok：正常
# #             unknow：找不到指定新闻
# #             error:未知错误


# 11
# 获取特定新闻 参数id
def get_news(request):
    if request.method == 'GET':
        news_id = request.GET.get('news_id') # 000
        the_news = models.News.objects.filter(id=news_id, active=True)

        if the_news:
            the_news = the_news[0]

            content = {'title': the_news.title,
                       'body': the_news.content,
                       'news_id': the_news.id,

                       # create_time
                       'pub_time': str(the_news.create_time.strftime('%Y-%m-%d %H:%M:%S')),
                       'update_time': str(the_news.update_time.strftime('%Y-%m-%d %H:%M:%S')),
                       'comment_num': the_news.commented_members,
                       'picture': the_news.picture.url,

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
            content = {'status': 'unknow'}

            content = json.dumps(content)

            return HttpResponse(content,
                                content_type='application/json;charset = utf-8',
                                status='404',
                                reason='Not_Found',
                                charset='utf-8')
    else:
        return HttpResponse(status=404)


# {
#   "num": "数量(int)",
#   "list": [{
#       "content": "评论内容",
#       "author_id": "作者id",
#       "author_name": "作者昵称",
#       "author_head": "作者头像url",
#       "time": "YYYY-MM-DD hh:mm:ss"
#   }],
#   "status": "ok"
# }
# status包含以下几种情况
# ok：正常
# null:新闻没有评论
# permission_dead:没有权限
# error:未知错误


# 11
# 获取评论列表 特定新闻
def get_commit_list(request):
    if request.method == 'GET':
        try:
            news_id = int(request.GET.get('news_id', default='0'))
        except ValueError:
            news_id = 0

        content = {'list': []}
        if news_id:
            news = models.News.objects.filter(id=news_id)[0]
            if news:
                all_comments_list = models.NewsComment.objects.filter(news=news).order_by('-create_time')

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
                        'author_id': one.author.id,
                        'author_name': one.author.username,
                        'author_head': one.author.head_image.url,
                        'time': str(one.create_time.strftime('%Y-%m-%d %H:%M:%S')),
                    })
                content['status'] = 'ok'

                content = json.dumps(content)

                return HttpResponse(content,
                                    content_type='application/json;charset = utf-8',
                                    status='200',
                                    reason='success',
                                    charset='utf-8')

            else:
                # 此新闻不存在
                content['num'] = 0
                content['status'] = 'error'

                content = json.dumps(content)

                return HttpResponse(content,
                                    content_type='application/json;charset = utf-8',
                                    status='404',
                                    reason='Not_Found',
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


# 00000000000000000
# 进行评论
def commit_news(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            json_data = {}
        except Exception:
            json_data = {}

        if json_data:
            # 验证用户登陆
            cookie = request.COOKIES()
            if cookie:

                # POST 的 内容验证
                ###########################
                if json_data['content']:
                    user = account_models.User.objects.filter(id=int(json_data['id']))[0]
                    news = models.News.objects.filter(id=int(json_data['id']))[0]

                    if user and news:

                        if models.NewsComment.objects.filter(author=user):


                            # 用户已评论
                            HttpResponse(status=404)
                        else:

                            models.NewsComment(news=news,
                                               author=user,
                                               content=json_data['content']
                                               ).save()
                            # 评论成功
                            HttpResponse(status=200)

                    else:
                        # 不存在 用户 或 新闻
                        HttpResponse(status=404)
                else:
                    # POST 数据错误
                    HttpResponse(status=404)
            else:
                # 未登录禁止评论
                HttpResponse(status=404)

        else:
            # 无此新闻
            HttpResponse(status=404)

    else:
        HttpResponse(status=404)


# 0
def delete_comment(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            json_data = {}
        except Exception:
            json_data = {}
        if json_data:
            cookie = request.COOKIES
            user = account_models.User.objects.filter(id=json_data['author_id'])
            # cookie 验证 用户
            ##########################################

            if user:
                user = user[0]
                comment = models.NewsComment.objects.filter(id=json_data['news_comment_id'],
                                                            author=user, active=True)
                if comment:
                    comment = comment[0]
                    comment.active = False

                    # 删除 是将 active = False
                    HttpResponse(status=200)
                else:
                    # 不存在此评论 或 用户不对等
                    HttpResponse(status=404)
            else:
                # 用户错误
                HttpResponse(status=404)
        else:
            # json 无数据
            HttpResponse(status=404)

    else:
        # method 错误
        HttpResponse(status=404)














