from .models import User
from account.models import User
import hashlib


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


'''用于对密码进行MD5加密的函数'''


def sign_password_md5(passwd, salt='kHa4sDk3dhQf'):
    hashpwd_builder = hashlib.md5()         # 构建md5加密器
    hashpwd_builder.update((passwd+salt).encode())
    return hashpwd_builder.hexdigest()      # 返回加密结果
