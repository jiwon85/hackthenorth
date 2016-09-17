from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^placeholder/$', views.index, name='index'),
]
