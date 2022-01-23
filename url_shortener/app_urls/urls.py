
from django.urls import re_path
from . import views

app_name = 'url_shortener'
urlpatterns = [
    re_path(r'^$', views.NewLinkView.as_view(), name='index'),
    re_path(r'^(?P<alias>[a-zA-Z0-9-_]+)$', views.redirect, name='alias'),
    re_path(r'^(?P<alias>[a-zA-Z0-9-_]+)(?P<extra>/.*)$', views.redirect, name='alias'),
    re_path(r'^(?P<alias>[a-zA-Z0-9-_]+)\+delete$', views.delete_link, name='delete_link'),
    re_path(r'^(?P<alias>[a-zA-Z0-9-_]+)\+$', views.preview, name='preview'),
    re_path(r'^~analytics/$', views.analytics, name='analytics'),
]
