from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'(?P<monster_uuid>[0-9a-f-]+)/$', views.detail, name='detail'),
]
