from .settings import verify_img, verify_email


'''
用于检擦图片验证码
参数：
    verify_id:验证码ID
    verify_code:验证码
返回值：
    0:验证码正确
    1:验证码错误
    2：验证码ID不存在
'''


def check_verify_img(verify_id, verify_code):
    if verify_id in verify_img:
        if verify_code == verify_img[verify_id]:
            return 0
        else:
            return 1
    else:
        return 2


def check_verify_email(verify_id, verify_code):
    if verify_id in verify_email:
        if verify_email[verify_id]['email'] == verify_email and verify_code == verify_email[verify_id]['code']:
            return 0
        else:
            return 1
    else:
        return 2
