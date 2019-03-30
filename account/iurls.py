"""mtime_itstudio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from account import views


urlpatterns = [
    # GET
    url(r'^user/info/(.+)',views.i_get_user_info),                    # 获取用户信息1
    # url(r'^user/film_review_list/(.+)'),        # 用户影评列表
    # url(r'^user/comments/(.+)'),               # 用户评论列表
    url(r'^user/comments_news/(.+)', views.i_get_user_comments_news_list),           # 用户新闻评论列表
    # url(r'^user/comments_filmreview/(.+)'),
    url(r'^logout/', views.i_logout),

    # POST
    url(r'^register', views.i_register),
    url(r'^login', views.i_login),
    url(r'^app_login', views.i_app_login),
    url(r'^changepasswd/(.+)', views.i_change_password),
    url(r'^foget_passwd', views.i_forgot_password),
]

