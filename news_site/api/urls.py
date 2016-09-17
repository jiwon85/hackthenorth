from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^placeholder/$', views.index, name='index'),
    # api
    url(r'^v1/articles/$', views.get_articles, name='get_articles')
]