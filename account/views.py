from django.shortcuts import render
from django.http import HttpResponse
from mtime_itstudio.general import check_verify_img, check_verify_email
from .account_user import to_register, sign_password_md5, get_json_dirt, check_dirt_args_valid, to_login, check_password_verify,check_user_id_verify
from news.models import NewsComment
from film.models import FilmReviewComment
from .models import User
import json
import datetime
import logging
import pickle

logger = logging.getLogger('account.view')


# 注册接口函数，尚未完成session and cookie
# 0:注册成功
# 1:用户ID重复
# 7:无效的用户ID
# 8:注册数据不完整
# 9:josn格式错误
def i_register(request):
    if request.method == 'POST':
        logger.info('收到post请求')
        # 读取post的内容
        # 使用try防止乱推出现异常崩溃
        try:
            post_body_json = json.loads(request.body)
            logger.debug('json解析成功')
        except json.JSONDecodeError:
            post_body_json = {}
            logger.error('json解析失败，收到POST:'+str(request.body))
            return HttpResponse("{\"result\":9}")
        except Exception:
            post_body_json = {}
            logger.error('json解析出现未知错误，收到POST:'+str(request.body))
            return HttpResponse("{\"result\":9}")

        # post判断post_body是否存在所需内容
        if post_body_json and \
                "user_id" in post_body_json and \
                'email' in post_body_json and\
                'user_name' in post_body_json and\
                'password' in post_body_json and\
                'verify_id' in post_body_json and\
                'verify_code' in post_body_json:
            logger.info('POST数据完整')
            # 检查验证码是否正确
            # 此处需要更换为email格式的验证码
            if True or check_verify_email(post_body_json['verify_id'], post_body_json['verify_code']):
                logger.debug('验证码检查通过')
                # 检查各项是否为空
                if not post_body_json['user_id']:
                    logger.info('空user_id')
                    return HttpResponse("{\"result\":7}")       # 无效的用户ID
                if not post_body_json['email']:
                    logger.info('空email')
                    return HttpResponse("{\"result\":6}")       # 等待添加错误标签
                if not post_body_json['password']:
                    logger.info('空密码')
                    return HttpResponse("{\"result\":5}")
                if not post_body_json['user_name']:
                    logger.info('空昵称')
                    return HttpResponse("{\"result\":4}")

                # 用户名密码合法性检查
                if not check_user_id_verify(post_body_json['user_id']):
                    logger.info('用户名不合法')
                    return HttpResponse("{\"result\":7}")
                if not check_password_verify(post_body_json['password']):
                    logger.info('密码不合法')
                    return HttpResponse("{\"result\":5}")

                # 写入数据库
                logger.info('将注册信息写入数据库')
                result, user = to_register(post_body_json['user_id'], post_body_json['user_name'], sign_password_md5(post_body_json['password']), post_body_json['email'])
                # 返回结果
                if not result:
                    # 注册成功
                    logger.info('返回注册成功')
                    response = HttpResponse("{\"result\":0}", status=200)
                    # 注册后自动登陆
                    try:
                        to_login(request, response, user)
                        logger.info('自动登陆完成')
                    except Exception:
                        logger.error('自动登陆出现异常')
                    return response
                else:
                    # 注册失败返回状态码
                    logger.error('注册失败返回状态码')
                    return HttpResponse("{\"result\":" + str(result) + "}}", status=200)

            else:
                # 验证码错误，返回状态码
                logger.info('验证码错误')
                return HttpResponse("{\"result\":3}", status=503)
        else:
            # post数据不完整，返回状态码
            logger.info('注册数据不完整')
            return HttpResponse("{\"result\":8}", status=503)
    else:
        # 非post请求，404
        logger.info('收到非POST请求')
        return HttpResponse(status=404)


# 登陆接口函数
# 2：无效的用户索引
# 5：无效的密码
# 8: 登陆数据缺失
# 9:json格式错误
def i_login(request):
    try:
        if request.method == 'POST':
            logger.info("收到POST请求")
            # 读取post的内容
            if 'user_id' not in request.session:
                # 使用try防止乱推出现异常崩溃
                try:
                    post_body_json = json.loads(request.body)
                    logger.info('解析json成功')
                except json.JSONDecodeError:
                    logger.error('json解析错误:' + str(request.body))
                    post_body_json = {}
                    return HttpResponse("{\"result\":9}")
                except Exception:
                    logger.error('json解析出现未知错误:' + str(request.body))
                    post_body_json = {}
                    return HttpResponse("{\"result\":9}")

                # post判断post_body是否存在所需内容
                if post_body_json and "user_key" in post_body_json and 'key_type' in post_body_json and \
                        'password' in post_body_json:
                    logger.debug('post数据完整')

                    # 检查各项是否为空
                    if not post_body_json['user_key'] or not post_body_json['key_type']:
                        # 无效的用户ID
                        logger.info('无效的用户索引')
                        return HttpResponse("{\"result\":2}")
                    if not post_body_json['password']:
                        # 无效的密码
                        logger.info('无效的密码')
                        return HttpResponse("{\"result\":5}")

                    # 查询用户，获取用户数据库对象
                    if post_body_json['key_type'] == 'user_id':
                        user = User.objects.filter(username=post_body_json['user_key'])
                    elif post_body_json['key_type'] == 'email':
                        user = User.objects.filter(email=post_body_json['user_key'])
                    else:
                        user = None
                        logger.info('无效的用户索引')
                        return HttpResponse("{\"result\":2}")
                    # 检索到用户
                    if user:
                        logger.info('检索到用户'+post_body_json['user_key'])
                        user = user[0]
                        if user.active:
                            if sign_password_md5(post_body_json['password']) == user.password:
                                response = HttpResponse("{\"result\":0}", status=200)
                                to_login(request, response, user)
                                return response
                            else:
                                # 密码错误
                                logger.info('密码错误')
                                return HttpResponse("{\"result\":2}", status=200)
                        else:
                            # active为Flase，账户被封禁
                            logger.info('账户被封禁')
                            return HttpResponse("{\"result\":4}")
                    else:
                        # 找不到用户，无效用户ID
                        logger.info('找不到用户：' + post_body_json['user_key'])
                        return HttpResponse("{\"result\":2}")
                else:
                    logger.info('post_body内容缺失')
                    return HttpResponse("{\"result\":8}")
            else:
                logger.info('已登录，请勿重复登陆')
                return HttpResponse("{\"result\":5}")
        else:
            # 非POST不接，返回404
            logger.info('app_login收到非post请求')
            return HttpResponse(status=404)
    except Exception:
        logger.error('出现未知错误')
        return HttpResponse("{\"result\":6}")


# 登出
def i_logout(request):
    if request.method == 'GET':
        if 'user_id' in request.session:
            logger.info(request.session['user_id']+'退出登录')
            request.session.flush()
            response = HttpResponse("{\"status\":\"ok\"}")
            try:
                response.delete_cookie('sessionid')
                response.delete_cookie('user_id')
                response.delete_cookie('user_nick')
            finally:
                pass
            return response
        else:
            return HttpResponse("{\"status\":\"not_logged_in\"}")


# 找回密码
def i_forgot_password(request, user_id):
    try:
        if request.method == 'POST':
            args_list = ('verify_id', 'verfiy_code', 'new_password')
            post_body_json = get_json_dirt(request.body, args_list)
            check_problem = check_dirt_args_valid(post_body_json, args_list)
            if not check_problem:
                if True or check_verify_email(post_body_json['verify_id'], post_body_json['verify_code']):
                    user = User.objects.filter(username=user_id)
                    user.password = sign_password_md5(post_body_json['new_password'])
                    user.save()
                    return HttpResponse("{\"result\":0}")
            elif check_problem == 'verify_id' or check_problem == 'verfiy_code':
                logger.info('缺少验证码'+check_problem)
                return HttpResponse("{\"result\":1}")
            elif check_problem == 'new_password':
                pass
        else:
            # 不接受非POST请求
            logger.info('收到非POST请求')
            return HttpResponse(status=404)
    except Exception:
        return HttpResponse("{\"result\":4}")


# 修改密码
def i_change_password(request, user_id):
    if request.method == 'POST':
        logger.info('收到post请求')
        logger.debug('user_id='+user_id)
        user = User.objects.filter(username=user_id)
        if not user or not ('user_id' in request.session and request.session['user_id'] == user_id):
            logger.info('未知用户或未登录')
            return HttpResponse("{\"result\": 3}")      # 返回未登录
        else:
            user = user[0]
            logger.info('已找到用户')
        args_list = ["old_password", "new_password", "verify_id", "verify_code"]
        # 安全解析json
        post_body = get_json_dirt(request.body, args_list)
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


# 上传头像
# 2:未找到对应文件
# 3：未登录
# 6：未知错误
def i_upload_head_img(request, filename):
    try:
        if request.method == 'POST':
            if 'user_id' in request.session:
                user = User.objects.filter(username=request.session['user_id'])
                if user:
                    user = user[0]
                    try:
                        f = request.FILES[filename]
                    except KeyError:
                        logger.info('未在request中找到对应文件')
                        return HttpResponse("{\"status\":\"2\"}", status=200)
                    try:
                        user.head_image = f
                        user.save()
                    except Exception:
                        logger.error('数据库写入失败')
                        return HttpResponse("{\"status\":\"6\"}", status=200)
                    # 成功返回0
                    return HttpResponse("{\"status\":\"0\"}", status=200)
                else:
                    return HttpResponse("{\"status\":\"3\"}", status=200)
            else:
                return HttpResponse("{\"status\":\"3\"}", status=200)
        else:
            logger.info('收到非post请求')
            return HttpResponse(status=404)
    except Exception:
        logger.error('出现未知错误')
        return HttpResponse("{\"status\":\"6\"}", status=500)


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
            logger.info('位置用户'+user_id)
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
                                               "title": comment['news__title'],
                                               "id": comment['news_id'],
                                               'image': "",
                                               'public_time': str(comment['create_time'].strftime('%Y-%m-%d %H:%M:%S'))})
                if comments_date_list:
                    logger.info('返回'+str(len(comments_date_list))+'条数据')
                    return HttpResponse([json.dumps({"num": len(comments_date_list),
                                                     'page': page,
                                                     "list": comments_date_list,
                                                     'total': total_num,
                                                     'status': 'ok'})])
                else:
                    logger.info('空列表')
                    return HttpResponse('{\"status\":\"none\"}')
            else:
                logger.error('未知用户：'+user_id)
                return HttpResponse('{\"status\":\"unknown_user\"}')
        else:
            logger.info('收到非POST请求')
            return HttpResponse(status=404)
    except Exception:
        logger.error('出现未知错误')
        return HttpResponse('{\"status\":\"error\"}')


# 用户影评评论列表
def i_get_user_film_review_comment_list(request, user_id):
    try:
        if request.method == 'GET':
            logger.info('接到get请求')
            user = User.objects.filter(username=user_id)
            if user:    # 检查用户是否存在
                logger.info('已检索到用户：'+str(user_id))
                user = user[0]

                # 获取切片分页信息
                page = request.GET.get('pages', '1')
                num = request.GET.get('num', '10')
                # 分页信息类型转换
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
                comments = FilmReviewComment.objects.select_related('film_review', 'film_review__film').filter(author_id=user.id).exclude(active=False). \
                    values('film_review_id', 'film_review__title', 'content', 'create_time', 'film_review__film__name')
                comments.reverse()      # 列表反向
                total_num = comments.count()    # 计算总评论数，以便计算页数
                # 分页切片
                comments = comments[(page-1)*num:page*num]
                comments_date_list = []
                for comment in comments:
                    comments_date_list.append({"content": comment['content'],
                                               "title": comment['film_review__title'],
                                               "film_name": comment['film_review__film__name'],
                                               'image': "",
                                               'review_id':comment['film_review_id'],
                                               'public_time': str(comment['create_time'].strftime('%Y-%m-%d %H:%M:%S'))})
                if comments_date_list:
                    logger.info('返回'+str(len(comments_date_list))+'条数据')
                    return HttpResponse([json.dumps({"num": len(comments_date_list),
                                                     'page': page,
                                                     "list": comments_date_list,
                                                     'total': total_num,
                                                     'status': 'ok'})])
                else:
                    logger.info('空列表')
                    return HttpResponse('{\"status\":\"none\"}')
            else:
                logger.error('未知用户：'+user_id)
                return HttpResponse('{\"status\":\"unknown_user\"}')
        else:
            logger.info('收到非POST请求')
            return HttpResponse(status=404)
    except Exception:
        logger.error('出现未知错误')
        return HttpResponse('{\"status\":\"error\"}')


# 用户影评列表
def i_film_review_list(request,user_id):
    try:
        if request.method == 'GET':
            pass
        else:
            logger.info('收到非get请求')
            return HttpResponse(status=404)
    except Exception:
        logger.error('出现未知错误')
        return HttpResponse('{\"status\":\"error\"}')
