#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

from django.conf import settings

from weblog.utils import cookie_to_user, cookie_to_view

class CookieMiddleware(object):
    
    '''middleware deal with cookies before each request'''
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        cookie = request.COOKIES.get(getattr(settings, 'COOKIE_NAME', ''), 'nothing')
        request.get_user = cookie_to_user(cookie)
        request.get_view = cookie_to_view(cookie)
        response = self.get_response(request)
        return response