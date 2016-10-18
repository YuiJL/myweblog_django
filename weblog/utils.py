#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

import hashlib, time, json
import requests

from datetime import datetime

from django.conf import settings
from django.http import HttpResponse

from weblog.models import User

def user_to_cookie(request, user, max_age=86400):
    
    '''
    return cookie from an user dict
    '''
    
    expire_time = str(max_age + int(time.time()))
    sha1_before = '%s-%s-%s-%s' % (user.next_id.hex, user.password, expire_time, getattr(settings, 'SECRET_KEY', ''))
    L = [user.next_id.hex, expire_time, hashlib.sha1(sha1_before.encode('utf-8')).hexdigest()]
    view_cookie = request.COOKIES.get(getattr(settings, 'COOKIE_NAME', ''), '').split('+').pop()
    return '-'.join(L) + '+' + view_cookie


def cookie_to_user(cookie):
    
    '''
    return an user dict from cookie
    '''
    
    try:
        L = cookie.split('+')[0].split('-')
        if len(L) != 3:
            return None
        next_id, expire_time, sha1 = L
        # cookie expired
        if int(time.time()) > int(expire_time):
            return None
        user = get_or_none(User, next_id=next_id)
        if not user:
            return None
        sha1_from_cookie = '%s-%s-%s-%s' % (user.next_id.hex, user.password, expire_time, getattr(settings, 'SECRET_KEY', ''))
        if sha1 != hashlib.sha1(sha1_from_cookie.encode('utf-8')).hexdigest():
            return None
        user.password = '********'
        return user
    except Exception as e:
        print(e)

        
def view_to_cookie(request, view):
    
    '''return cookie from query string'''
    
    user_cookie = request.COOKIES.get(getattr(settings, 'COOKIE_NAME', ''), '').split('+')[0]
    return user_cookie + '+' + view


def cookie_to_view(cookie):
    
    '''extract view mode from cookie'''
    
    view = cookie.split('+').pop()
    if not view:
        return None
    return view


def check_recaptcha(secret, response):
    
    '''
    check if user is bot by a POST request to Google recaptcha api
    '''
    
    url = 'https://www.google.com/recaptcha/api/siteverify'
    data = {'secret': secret, 'response': response}
    try:
        jsonobj = json.loads(requests.post(url, data=data).text)
        if jsonobj['success']:
            return True
        else:
            return False
    except Exception as e:
        return False
    

def valid_password(user, password):
    
    '''
    verify password
    '''
    
    if password is None:
        return False
    sha1 = hashlib.sha1()
    sha1.update(password.encode('utf-8'))
    sha1.update(user.email.encode('utf-8'))
    sha1.update(b'the-Salt')
    return sha1.hexdigest() == user.password


def allowed_file(filename):
    
    '''allowed extension for uploaded files'''
    
    return '.' in filename and filename.rsplit('.', 1)[1] in getattr(settings, 'ALLOWED_EXTENSIONS', set())


def get_or_none(model, *args, **kw):
    
    '''
    a wrapper for model.objects.get
    '''
    
    try:
        return model.objects.get(*args, **kw)
    except model.DoesNotExist:
        return None