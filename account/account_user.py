from .models import User
from account.models import User
import hashlib
import json
import datetime


'''
返回值
    0:注册成功
    1：用户id重复
    2：邮箱已被注册
'''


def to_register(user_id, user_name, password, email):
    if User.objects.filter(username=user_id):
        return 1
    if User.objects.filter(email=email):
        return 2
    User(username=user_id, password=password, email=email, nickname=user_name).save()
    return 0


# '''用于对密码进行MD5加密的函数'''
def sign_password_md5(passwd, salt='kHa4sDk3dhQf'):
    hashpwd_builder = hashlib.md5()         # 构建md5加密器
    hashpwd_builder.update((passwd+salt).encode())
    return hashpwd_builder.hexdigest()      # 返回加密结果


# 用于安全的获取json内容
def get_json(data_str, args_list):
    # 读取post的内容
    # 使用try防止乱推出现异常崩溃
    try:
        post_body_json = json.loads(data_str)
    except json.JSONDecodeError:
        return {}
    except Exception:
        return {}

    for arg in args_list:
        if arg not in post_body_json:
            return {}
    return post_body_json


# 检查dirt中各个元素是否有效
# 若无效，则返回无效元素名称
# 若全部有效，则返回空字符串
def check_dirt_args_valid(json_dirt, args_list):
    for arg in args_list:
        if not json_dirt[arg]:
            return arg
    return ''


# 用于登录的函数
def to_login(request, user):
    request.session['user_id'] = user.id
    request.session['login_key'] = sign_password_md5(str(datetime.datetime.now()))
