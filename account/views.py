from django.shortcuts import render
from django.http import HttpResponse
from mtime_itstudio.general import check_verify_img
from .account_user import to_register, sign_password_md5, get_json, check_dirt_args_valid, to_login
from news.models import NewsComment
from .models import User
import json
import datetime
import logging
import pickle

logger = logging.getLogger('account.view')


# 注册接口函数，尚未完成session and cookie
def i_register(request):
    if request.method == 'POST':
        logger.info('收到post请求')
        # 读取post的内容
        # 使用try防止乱推出现异常崩溃
        try:
            post_body_json = json.loads(request.body)
            logger.debug('i_register收到POST:'+str(post_body_json))
        except json.JSONDecodeError:
            post_body_json = {}
            logger.error('i_register解析失败，收到POST:'+str(post_body_json))
        except Exception:
            post_body_json = {}
            logger.error('i_registerPost解析出现未知错误，收到POST:'+ str(post_body_json))

        # post判断post_body是否存在所需内容
        if post_body_json and \
                "user_id" in post_body_json and \
                'email' in post_body_json and\
                'user_name' in post_body_json and\
                'password' in post_body_json and\
                'verify_id' in post_body_json and\
                'verify_code' in post_body_json:
            logger.info('POST数据正常')
            # 检查验证码是否正确
            # 此处需要更换为email格式的验证码
            if True or check_verify_img(post_body_json['verify_id'], post_body_json['verify_code']):
                logger.info('验证码通过')

                # 检查各项是否为空
                if not post_body_json['user_id']:
                    return HttpResponse("{\"result\":7}")
                if not post_body_json['email']:
                    return HttpResponse("{\"result\":6}")       # 等待添加错误标签
                if not post_body_json['password']:
                    return HttpResponse("{\"result\":5}")
                if not post_body_json['user_name']:
                    return HttpResponse("{\"result\":4}")

                # 写入数据库
                logger.info('将注册信息写入数据库')
                result, user = to_register(post_body_json['user_id'], post_body_json['user_name'], sign_password_md5(post_body_json['password']), post_body_json['email'])
                # 返回结果
                if not result:
                    # 注册成功
                    logger.info('注册成功')
                    # 注册后自动登陆
                    to_login(request, user)
                    return HttpResponse("{\"result\":0}", status=200)
                else:
                    # 注册失败返回状态码
                    return HttpResponse("{\"result\":" + str(result) + "}}", status=200)

            else:
                # 验证码错误，返回状态码
                return HttpResponse("{\"result\":3}", status=503)
        else:
            # post数据不完整，返回状态码
            return HttpResponse("{\"result\":6}", status=503)
    # 非post请求，404
    return HttpResponse(status=404)


# 登陆接口函数
def i_login(request):
    if request.method == 'POST':
        logger.info('收到post请求')
        # 读取post的内容
        # 使用try防止乱推出现异常崩溃
        try:
            post_body_json = json.loads(request.body)
        except json.JSONDecodeError:
            post_body_json = {}
        except Exception:
            post_body_json = {}

        # post判断post_body是否存在所需内容
        if post_body_json and ("user_id" in post_body_json or 'email' in post_body_json) and \
                'password' in post_body_json and \
                'verify_id' in post_body_json and \
                'verify_code' in post_body_json:

            # 检查验证码
            if True or check_verify_img(post_body_json['verify_id'], post_body_json['verify_code']):

                # 检查各项是否为空
                if not post_body_json['user_id'] and not post_body_json['emial']:
                    # 无效的用户ID
                    return HttpResponse("{\"result\":2}")
                if not post_body_json['password']:
                    # 无效的密码
                    return HttpResponse("{\"result\":5}")

                user = User.objects.filter(username=post_body_json['user_id'])
                if user:
                    user = user[0]
                    if user.active:
                        if sign_password_md5(user.password) == post_body_json['password']:
                            request.session['login_session'] = post_body_json['user_id'] + str(datetime.datetime.now())
                            return HttpResponse("{\"result\":0}", status=200)
                        else:
                            # 密码错误
                            return HttpResponse("{\"result\":2}", status=200)
                    else:
                        # active为Flase，账户被封禁
                        return HttpResponse("{\"result\":4}")
                else:
                    # 找不到用户，无效用户ID
                    return HttpResponse("{\"result\":2}")
        else:
            return HttpResponse("{\"result\":6}")
    # 非POST不接，返回404
    return HttpResponse(status=404)


def i_app_login(request):
    if request.method == 'POST':
        logger.info("收到POST请求")
        # 读取post的内容

        # 使用try防止乱推出现异常崩溃
        try:
            post_body_json = json.loads(request.body)
        except json.JSONDecodeError:
            post_body_json = {}
        except Exception:
            post_body_json = {}

        # post判断post_body是否存在所需内容
        if post_body_json and ("user_id" in post_body_json or 'email' in post_body_json) and \
                'password' in post_body_json and \
                'verify_id' in post_body_json and \
                'verify_code' in post_body_json:

            # 检查各项是否为空
            if not post_body_json['user_id'] and not post_body_json['emial']:
                # 无效的用户ID
                return HttpResponse("{\"result\":2}")
            if not post_body_json['password']:
                # 无效的密码
                return HttpResponse("{\"result\":5}")
            # 查询用户，获取用户数据库对象
            user = User.objects.filter(username=post_body_json['user_id'])
            if user:
                user = user[0]
                if user.active:
                    if sign_password_md5(user.password) == post_body_json['password']:
                        request.session['login_session'] = post_body_json['user_id'] + str(datetime.datetime.now())
                        return HttpResponse("{\"result\":0}", status=200)
                    else:
                        # 密码错误
                        return HttpResponse("{\"result\":2}", status=200)
                else:
                    # active为Flase，账户被封禁
                    return HttpResponse("{\"result\":4}")
            else:
                # 找不到用户，无效用户ID
                return HttpResponse("{\"result\":2}")
        else:
            return HttpResponse("{\"result\":6}")
    # 非POST不接，返回404
    return HttpResponse(status=404)


def i_logout(request):
    pass


def i_forgot_password(request, user_id):
    pass


def i_change_password(request, user_id):
    if request.method == 'POST':
        logger.info('收到post请求')
        logger.debug('user_id='+user_id)
        user = User.objects.filter(username=user_id)
        if not user or not ('user_id' in request.session and request.session['user_id'] == user_id):
            logger.info('位置用户或未登录')
            return HttpResponse("{\"result\": 3}") # 返回未登录
        else:
            user = user[0]
            logger.info('已找到用户')
        args_list = ["old_password", "new_password", "verify_id", "verify_code"]
        # 安全解析json
        post_body = get_json(request.body, args_list)
        logger.debug('json已解析')
        # 检查元素合法
        check_problem = check_dirt_args_valid(post_body, args_list)
        if not check_problem:
            logger.info('json验证通过')
            if sign_password_md5(post_body['old_password']) == user.password:
                user.password = sign_password_md5(post_body['new_password'])
                user.save()
                logger.info('密码修改成功')
                return HttpResponse("{\"result\": 0}")
        else:
            if check_problem == 'old_password':
                return HttpResponse("{\"result\": 1}")
            elif check_problem == 'new_password':
                return HttpResponse("{\"result\": 4}")  # 新密码不存在的状态等待定义
            elif check_problem == 'verify_id' or check_problem == 'verify_code':
                return HttpResponse("{\"result\": 2}")


'''GET'''


# 获取用户信息
def i_get_user_info(request, user_id):
    if request.method == 'GET':
        logger.info('收到GET请求')
        user = User.objects.filter(username=user_id)        # 从数据库中检索用户
        if user:        # 检查用户是否存在
            user = user[0]
            data = {"user_id": user.username,
                    "username": user.nickname,
                    'head':"",
                    "email": user.username,
                    'status':'ok'}
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse("{\"status\": \"unknow_user\"}")


# 用户新闻评论列表
def i_get_user_comments_news_list(request, user_id):
    try:
        if request.method == 'GET':
            logger.info('接到get请求')
            user = User.objects.filter(username=user_id)
            if user:    # 检查用户是否存在
                logger.info('已检索到用户：'+str(user_id))
                user = user[0]

                # 获取切片信息
                page = request.GET.get('pages', '1')
                num = request.GET.get('num', '10')
                try:
                    num = int(num)
                except TypeError:
                    logger.error('num类型转换异常')
                    num = 10
                try:
                    page = int(page)
                except TypeError:
                    logger.error('page类型转换异常')
                    page = 1
                logger.info('拉取第'+str(page)+'页，每页'+str(num)+'个数据')

                # 搜索数据库
                comments = NewsComment.objects.select_related('news').filter(author_id=user.id).exclude(active=False).\
                    values('news_id', 'news__title', 'content', 'create_time')
                comments.reverse()      # 列表反向
                total_num = comments.count()    # 计算总评论数，以便计算页数
                comments = comments[(page-1)*num:page*num]
                comments_date_list = []
                for comment in comments:
                    comments_date_list.append({"content": comment['content'],
                                               "titel": comment['news__title'],
                                               "id": comment['news_id'],
                                               'image': "",
                                               'public_time': str(comment['create_time'])})
                logger.info('返回'+str(num)+'条数据')
                return HttpResponse([json.dumps({"num": len(comments_date_list),
                                                 'page': page,
                                                 "list": comments_date_list,
                                                 'total': total_num,
                                                 'status': 'ok'})])
            else:
                logger.error('未知用户：'+user_id)
                return HttpResponse('{\"status\":\"unknown_user\"}')
    except Exception:
        logger.error('出现未知错误')
        return HttpResponse('{\"status\":\"error\"}')
