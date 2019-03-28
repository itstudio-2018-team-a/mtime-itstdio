from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^news/i/hotpot_list', views.get_hotpot_list),
    # url(r'^')
]
