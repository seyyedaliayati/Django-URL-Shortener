
from django.urls import re_path
from . import views

app_name = 'app_urls'
urlpatterns = [
    re_path(r'^$', views.NewLinkView.as_view(), name='index'),
    re_path(r'^(?P<alias>[a-zA-Z0-9-_]+)$', views.LinkRedirectView.as_view(), name='alias'),
    re_path(r'^(?P<alias>[a-zA-Z0-9-_]+)(?P<extra>/.*)$', views.LinkRedirectView.as_view(), name='alias'),
    re_path(r'^(?P<alias>[a-zA-Z0-9-_]+)\+delete$', views.DeleteLinkView.as_view(), name='delete'),
    re_path(r'^(?P<alias>[a-zA-Z0-9-_]+)\+update$', views.LinkUpdateView.as_view(), name='update'),
    re_path(r'^(?P<alias>[a-zA-Z0-9-_]+)\+chart$', views.ChartDataView.as_view(), name='chart_data'),
    re_path(r'^(?P<alias>[a-zA-Z0-9-_]+)\+$', views.LinkPreview.as_view(), name='preview'),
    re_path(r'^~analytics/$', views.AnalyticsView.as_view(), name='analytics'),
]
