"""exp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^v1/create/', views.create, name='create'),
    url(r'^v1/signup/', views.signup, name='signup'),
    url(r'^v1/login/', views.login, name='login'),
    url(r'^v1/get_details/(?P<id>[0-9]+)/$', views.get_details, name='get_details'),
    url(r'^v1/home/', views.get_data, name='index'),
    url(r'^v1/top/', views.get_top_data, name='top'),
    url(r'^v1/price/', views.get_price_data, name='price'),
    url(r'^v1/delete/(?P<id>[0-9]+)/$', views.delete, name='delete'),
    url(r'^v1/update/(?P<id>[0-9]+)/$', views.update, name='update'),
    url(r'^admin/', admin.site.urls),
]
