from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'api'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'v1/list/', views.get_list, name='get_list'),
    url(r'v1/top_list/', views.get_top_list, name='get_top_list'),
    url(r'v1/price_list/', views.get_price_list, name='get_price_list'),
    url(r'v1/create/', views.create, name='create'),
    url(r'v1/signup/', views.signup, name='signup'),
    url(r'v1/login/', views.login, name='login'),
    url(r'v1/logout/', views.logout, name='logout'),
    url(r'v1/auth/', views.auth, name='auth'),
    url(r'v1/delete/(?P<id>[0-9]+)/$', views.delete, name='delete'),
    url(r'v1/update/(?P<id>[0-9]+)/$', views.update, name='update'),
    url(r'v1/item/(?P<id>[0-9]+)/$', views.item, name='item'),
    url(r'v1/profile/(?P<username>\w{0,50})/$', views.profile, name='profile'),
]
