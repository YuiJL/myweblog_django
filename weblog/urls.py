from django.conf.urls import url

from weblog import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]