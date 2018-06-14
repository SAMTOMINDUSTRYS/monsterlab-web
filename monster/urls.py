from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'monster/(?P<monster_uuid>[0-9a-f-]+)/$', views.detail, name='detail'),
    url(r'^allele/(?P<variant_uuid>[0-9a-f-]+)/$', views.list_monster_allele, name='list_monster_allele'),
    url(r'^allele/(?P<variant_uuid>[0-9a-f-]+)/(?P<allele>[A-z]+)/$', views.list_monster_allele, name='list_monster_allele'),
    url(r'^hallele/(?P<variant_uuid>[0-9a-f-]+)/(?P<allele>[A-z]+)/$', views.list_monster_hallele, name='list_monster_hallele'),
    url(r'^fasta/$', views.fasta, name='fasta'),
    url(r'^matrix/$', views.matrix, name='matrix'),
]
