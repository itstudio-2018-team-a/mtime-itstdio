from django.conf.urls import url
from . import views

urlpatterns = [
    # 今日热点列表（最多10个） GET
    # required: null
    # selected: null
    url(r'^i/hotpot_list/', views.get_hotpot_list),

    # 全部新闻列表 GET
    # required: null
    # selected: page=?(default=1) num=?(default=10)
    url(r'^i/news_list/', views.get_all_news),

    # 新闻内容 GET
    # required: news_id=?
    # selected: null
    url(r'^i/news/$', views.get_news),

    # 新闻评论列表
    # required: news_id=?
    # selected: page=?(default=1) num=?(default=10)
    url(r'^i/comment_list/', views.get_commit_list),

    # url(r'^comment/i/')
]
