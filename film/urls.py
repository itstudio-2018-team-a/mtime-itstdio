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

from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # 电影列表 GET
    # required: null
    # selected: page=?(default=1) num=?(default=10)
    url(r'^i/film_list/', views.get_film_list),

    # 电影内容 GET
    # required: film_id=?
    # selected: null
    url(r'^i/film/', views.get_film),

    # 正在上映的电影 GET
    # required: null
    # selected: null
    url(r'^i/ticketing_film/', views.get_on_movie),

    # 即将上映的电影 GET
    # required: null
    # selected: null
    url(r'^i/coming_film/', views.get_coming_movie),

    # 影评列表 GET
    # required: null
    # selected: page=?(default=1) num=?(default=10)
    url(r'^i/film_review_list', views.get_film_review_list),

    # 影评内容 GET
    # required: review_id=?
    # selected: null
    url(r'^i/film_review/$', views.get_review),

    # 热门影评 GET
    # required: null
    # selected: null
    url('^i/hot_review_list/', views.get_hot_review),

    # 短评 GET
    # required: film_id=?
    # selected: page=?(default=1) num=?(default=10)
    url(r'^i/short_comment_list/', views.get_short_comment),

    #  影评评论 GET
    # required: review_id=?
    # selected: page=?(default=1) num=?(default=10)
    url(r'^i/film_review_comment', views.get_review_comment),

    # 获取评分 GET
    # required: film_id=?
    # selected: null
    url(r'^i/film_score?$', views.get_score)

]


