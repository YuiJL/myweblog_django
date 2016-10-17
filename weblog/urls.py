#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

from django.conf.urls import url

from weblog import views

app_name = 'weblog'

urlpatterns = [
    # /
    url(r'^$', views.index, name='index'),
    # /blogs/<page>/
    url(r'^blogs/(?P<page>[0-9]+)/$', views.blog_list, name='blog_list'),
    # /blog/<auto_id>/
    url(r'^blog/(?P<auto_id>[0-9]+)/$', views.single_blog, name='single_blog'),
    # /register/
    url(r'^register/$', views.register, name='register'),
    # /signout/
    url(r'^signout/$', views.sign_out, name='sign_out'),
    # /auth/
    url(r'^auth/$', views.auth, name='auth'),
    # /blog/new/
    url(r'^blog/new/(?P<auto_id>[0-9]*)$', views.blog_post, name='blog_post'),
    # /blog/<auto_id>/edit/
    url(r'^blog/(?P<auto_id>[0-9]+)/edit/$', views.blog_post, name='blog_post'),
    # /api/blog/<auto_id>/
    url(r'^api/blog/(?P<auto_id>[0-9]*)/?$', views.api_blog, name='api_blog'),
    # /api/blog/<auto_id>/comments/
    url(r'^api/blog/(?P<auto_id>[0-9]+)/comments/$', views.api_blog_comment, name='api_blog_comment'),
    # /api/blog/<auto_id>/comments/<comment_id>/
    url(r'^api/blog/(?P<auto_id>[0-9]+)/comments/(?P<comment_id>[0-9]+)/$', views.api_subcomment, name='api_subcomment'),
    # /api/<key>/<id>/delete/
    url(r'^api/(?P<key>comments|subcomments)/(?P<id>[0-9]+)/delete/$', views.delete, name='delete'),
]