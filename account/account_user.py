from .models import User
from account.models import User


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
