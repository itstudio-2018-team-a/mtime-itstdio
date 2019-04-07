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
from .general import i_get_email_verify_code
from .general import return_index
from .general import return_register
from .general import return_login
from .general import return_personal_page
from .general import return_find_back

from .general import return_index, css_redirect, templates_redirect, js_redirect, dist_redirect, redirect_index


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^account/', include('account.urls', namespace='Account')),
    url(r'^news/', include('news.urls', namespace='news')),
    url(r'^film/', include('film.urls', namespace='film')),
    url(r'i/email_verify_code', i_get_email_verify_code),

    url(r'^index/$', return_index),
    url(r'^index/(.+)', redirect_index),
    url(r'^login', return_login),
    url(r'^register', return_register),
    url(r'^personal_page', return_personal_page),
    url(r'^find_back', return_find_back),

    url(r'^templates/(.+)', templates_redirect),
    url(r'^js/(.+)', js_redirect),
    url(r'^css/(.+)', css_redirect),
    url(r'^dist/(.+)', dist_redirect),

    url(r'^$', return_index)

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL)
