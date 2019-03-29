from django.shortcuts import render
from django.http import HttpResponse
from mtime_itstudio.general import check_verify_img
from .account_user import to_register, sign_password_md5
from .models import User
import json
import datetime
import logging


logger = logging.getLogger('account')


'''
注册接口函数，尚未完成session and cookie
'''


def i_register(request):
    if request.method == 'POST':
        # 读取post的内容
        # 使用try防止乱推出现异常崩溃
        try:
            post_body_json = json.loads(request.body)
            logger.debug('i_register收到POST:', str(post_body_json))
        except json.JSONDecodeError:
            logger.error('i_register解析失败，收到POST:', str(post_body_json))
            post_body_json = {}
        except Exception:
            logger.error('i_registerPost解析出现未知错误，收到POST:', str(post_body_json))
            post_body_json = {}

        # post判断post_body是否存在所需内容
        if post_body_json and \
                "user_id" in post_body_json and \
                'email' in post_body_json and\
                'user_name' in post_body_json and\
                'password' in post_body_json and\
                'verify_id' in post_body_json and\
                'verify_code' in post_body_json:
            logger.debug('POST数据正常')
            # 检查验证码是否正确
            # 此处需要更换为email格式的验证码
            if True or check_verify_img(post_body_json['verify_id'], post_body_json['verify_code']):
                logger.debug('验证码通过')

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
                logger.debug('将注册信息写入数据库')
                result = to_register(post_body_json['user_id'], post_body_json['user_name'], sign_password_md5(post_body_json['password']), post_body_json['email'])

                # 返回结果
                if not result:
                    # 注册成功
                    logger.debug('注册成功')
                    logger.debug('开始写入session')
                    request.session['login_session'] = post_body_json['user_id'] + str(datetime.datetime.now())
                    logger.debug('session写入成功')
                    return HttpResponse("{\"result\":0}", status=200)
                else:
                    # 注册失败返回状态码
                    return HttpResponse("{\"result\":{0}}".format(result), status=200)

            else:
                # 验证码错误，返回状态码
                return HttpResponse("{\"result\":3}", status=503)
        else:
            # post数据不完整，返回状态码
            return HttpResponse("{\"result\":6}", status=503)
    # 非post请求，404
    return HttpResponse(status=404)


'''登陆接口函数'''


def i_login(request):
    if request.method == 'POST':

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


def i_forgot_password(request):
    pass


def i_change_password(request):
    pass
