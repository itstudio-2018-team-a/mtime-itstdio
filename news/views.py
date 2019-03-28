from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
import json
# Create your views here.
from . import models
from account import models as account_models


# 获取热点新闻
def get_hotpot_list(request):
    if request.method == 'GET':
        hot_news = models.News.objects.all().order_by('-hits', '-create_time')[:10]

        json_data = json.dumps(hot_news)

        HttpResponse(json_data)
    else:
        HttpResponse(status=404)


# 获取全部新闻列表
def get_all_news(request):
    if request.method == 'GET':
        all_news_list = models.News.objects.all()

        # 分页器 每页 10 个新闻
        paginator = Paginator(all_news_list, 10)

        try:
            page_num = int(request.GET.get('page', default='1'))
        except ValueError:
            page_num = 1

        max_page_num = paginator.count()
        if page_num > max_page_num:
            page_num = max_page_num
        if page_num < 1:
            page_num = 1

        page_of_list = paginator.page(page_num)
        content = {}
        content['list'] = page_of_list.object_list

        content['max_page'] = max_page_num

        json_data = json.dumps(content)
        HttpResponse(json_data)

    else:
        HttpResponse(status=404)


# 获取特定新闻 参数id
def get_news(request, news_id):
    if request.method == 'GET':
        the_news = models.News.objects.filter(id=news_id, active=True)[0]

        if the_news:
            result = {}
            result['title'] = the_news.title
            result['author'] = the_news.author.username
            result['author_id'] = the_news.author_id
            result['content'] = the_news.content
            result['create_time'] = the_news.create_time
            result['update_time'] = the_news.update_time
            result['hits'] = the_news.hits
            result['commented_member'] = the_news.commented_members
            result['picture'] = the_news.picture

            json_data = json.dumps(result)

            HttpResponse(json_data)

        else:
            # 返回错误信息
            #########
            HttpResponse(status=404)
    else:
        HttpResponse(status=404)


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


# 获取评论列表 特定新闻
def get_commit_list(request):
    if request.method == 'GET':
        try:
            news_id = int(request.GET.get('news_id', default='0'))
        except ValueError:
            news_id = 0
        if news_id:
            news = models.News.objects.filter(id=news_id)[0]
            if news:
                all_comments = models.NewsComment.objects.filter(news=news)

                result = {}
                result['list'] = all_comments

                json_data = json.dumps(result)

                HttpResponse(json_data)
            else:
                # 此新闻不存在
                HttpResponse(status=404)
        else:
            # news_id 不正确
            HttpResponse(status=404)

    else:
        HttpResponse(status=404)


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














