from .settings import verify_img, verify_email
from django.core.mail import send_mail
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect
from account.account_user import check_email_verify
import random
import time
import _thread
import logging
from django.shortcuts import render, redirect

logger = logging.getLogger('general')

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
    vc = cache.get(verify_id, {})
    if vc:
        if verify_code == vc['code']:
            return 0
        else:
            return 1
    else:
        return 2


def to_send_email_verify_code(to_email):

    # 生成验证码
    code = str(random.randint(100000, 999999))
    logger.debug("验证码生成")
    # 发送邮件部分
    send_mail(
        'ITStudio Mtime A组 验证码',
        '您的验证码为：'+code+",验证码在60分钟内有效（请勿回复）",
        'itstudiomtimea@163.com',
        [to_email],
        fail_silently=False,
    )
    logger.debug('邮件发送成功')
    cache.set(to_email, {'sent_time': time.time(), 'code': code}, 3600)


def i_get_email_verify_code(request):
    if request.method == 'GET':
        logger.debug('收到GET请求')
        email = request.GET.get('email', '')
        # 检查邮箱是否为空
        if check_email_verify(email):

            # 检查该邮箱是否存在于缓存
            c = cache.get(email)
            if c:
                if time.time() - c['sent_time'] < 60:
                    return HttpResponse("{\"status\":\"too_fast\"}")

            # 满足条件发送邮件
            _thread.start_new_thread(to_send_email_verify_code, (email,))
            logger.debug("创建新线程发送邮件")
            return HttpResponse("{\"id\":\""+email+"\",\"wait\":60,\"status\":\"ok\"}")
        else:
            # 邮箱不合法
            logger.info("邮箱不合法")
            return HttpResponse("{\"status\":\"invalid_email\"}")
    else:
        logger.info('收到非GET请求')
        return HttpResponse(status=404)


def return_index(request):
    return render(request, 'dist/index.html')

def redirect_index(requset, left_url):
    return redirect('/' + left_url)


def return_login(request):
    return render(request, 'dist/logIn.html')


def return_register(request):
    return render(request, 'dist/register.html')


def return_personal_page(request):
    return render(request, 'dist/PersonalPage.html')


def return_find_back(request):
    return render(request, 'dist/findBack.html')


def templates_redirect(requset, left_url):
    return redirect('/static/templates/'+left_url)


def js_redirect(requset, left_url):
    return redirect('/static/js/'+left_url)


def css_redirect(requset, left_url):
    return redirect('/static/css/'+left_url)


def dist_redirect(requset, left_url):
    return redirect('/static/dist/'+left_url)


