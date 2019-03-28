from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^i/hotpot_list/', views.get_hotpot_list),
    url(r'^i/get_all_new/', views.get_all_news),
    url(r'^i/news/$', views.get_news),
    # url(r'^comment/i/')
]
