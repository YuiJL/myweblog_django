#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

import math, uuid

from datetime import datetime

from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from weblog.models import Blog, Comment, Subcomment, User
from weblog.utils import user_to_cookie, view_to_cookie, check_recaptcha, valid_password, get_or_none


#**************************************************************
#----------------Homepage, Blog and Manage Page----------------
#**************************************************************


def index(request):
    
    '''homepage'''
    
    blog_list = Blog.objects.order_by('-post_date')
    pages = [str(i) for i in range(1, math.ceil(len(blog_list) / 10) + 1)]
    blog_list = blog_list[:10]
    context = {
        'blog_list': blog_list,
        'pages': pages,
        'page': '1',
        'labels': ['primary', 'success', 'info', 'warning', 'danger'],
    }
    
    if request.method == 'GET':
        return render(request, 'weblog/blogs.html', context)
    else:
        # return a response with cookie which contains info of view mode
        view_mode = request.GET.get('view')
        cookie = view_to_cookie(request, view_mode)
        response = HttpResponse()
        response.set_cookie(getattr(settings, 'COOKIE_NAME', ''), cookie, max_age=86400, httponly=True)
        return response


def blog_list(request, page):
    
    '''show blogs by pages'''
    
    start = 10 * (int(page) - 1)
    blog_list = Blog.objects.order_by('-post_date')
    pages = [str(i) for i in range(1, math.ceil(len(blog_list) / 10) + 1)]
    blog_list = blog_list[start:start+10]
    context = {
        'blog_list': blog_list,
        'pages': pages,
        'page': page,
        'labels': ['primary', 'success', 'info', 'warning', 'danger'],
    }
    return render(request, 'weblog/blogs.html', context)


def single_blog(request, auto_id):
    
    '''single blog page'''
    
    blog = get_object_or_404(Blog, auto_id=auto_id)
    context = {
        'blog': blog,
        'labels': ['primary', 'success', 'info', 'warning', 'danger'],
    }
    return render(request, 'weblog/blog.html', context)


def blog_post(request, auto_id):
    
    '''new post / blog edit page'''
    
    if request.get_user and request.get_user.admin:
        return render(request, 'weblog/edit.html')
    else:
        return HttpResponseRedirect(reverse('weblog:index'))
    
    
#**************************************************************
#----------------Login, Signout, Authentication----------------
#**************************************************************


def register(request):
    
    '''
    register a new account
    '''
    
    if request.method == 'GET':
        if request.get_user:
            return HttpResponseRedirect(reverse('weblog:index'))
        else:
            return render(request, 'weblog/register.html', {'site_key': getattr(settings, 'RECAPTCHA_SITE_KEY', '')})
    else:
        name = request.POST.get('name')
        if get_or_none(User, name=name):
            return HttpResponse('Username is taken, please try another.', status=400)
                                                        
        email = request.POST.get('email')
        if get_or_none(User, email=email):
            return HttpResponse('E-mail is taken, please try another.', status=400)
                                                        
        recaptcha_response = request.POST.get('recaptcha')
        if not check_recaptcha(getattr(settings, 'RECAPTCHA_SECRET_KEY', ''), recaptcha_response):
            return HttpResponse("You're a bot.", status=400)
                                                        
        password = request.POST.get('sha1_password')
        user = User(name=name, email=email, password=password, created=timezone.now())
        user.next_id = uuid.uuid4()
        user.set_sha1()
        user.save()
        
        cookie = user_to_cookie(request, user)
        response = HttpResponse()
        response.set_cookie(getattr(settings, 'COOKIE_NAME', ''), cookie, max_age=86400, httponly=True)
        return response


def auth(request):
    
    '''
    authenticate an user, return a login response with cookie (if success)
    '''
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('sha1_password')
        user = get_or_none(User, email=email)
        if user is None:
            return HttpResponse('E-mail not found', status=403)
        if not valid_password(user, password):
            return HttpResponse('Wrong password', status=403)
        cookie = user_to_cookie(request, user)
        response = HttpResponse()
        response.set_cookie(getattr(settings, 'COOKIE_NAME', ''), cookie, max_age=86400, httponly=True)
        return response
    
    
def sign_out(request):
    
    '''return a sign out response'''
    
    cookie = request.COOKIES.get(getattr(settings, 'COOKIE_NAME', '').split('+').pop())
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie(getattr(settings, 'COOKIE_NAME', ''), '+' + cookie, max_age=86400, httponly=True)
    return response


#************************************
#----------------APIs----------------
#************************************


def api_blog_comment(request, auto_id):
    
    '''
    all about comments from a single blog
    '''
    
    blog = get_object_or_404(Blog, auto_id=auto_id)
    
    if request.method == 'POST':
        if not request.get_user:
            return HttpResponse('Please sign in', status=403)
        content = request.POST.get('content', '').lstrip('\n').rstrip()
        if not content:
            return HttpResponse('Content cannot be empty.', status=403)
        blog.comment_set.create(user_id=request.get_user.id, content=content, post_date=timezone.now())
    
    comments = blog.comment_set.order_by('-post_date')
    result = []
    for c in comments:
        t = int(c.post_date.timestamp())
        dt = datetime.fromtimestamp(t).strftime('%I:%M:%S %p, %a, %b %d, %Y')
        c_dict = dict(user=c.user.name, image=c.user.image, content=c.content, post_date=dt, id=c.id)
        if not c.subcomment_set.all():
            c_dict.update(subcomment=[])
        else:
            subcomment = []
            for sub in c.subcomment_set.order_by('post_date'):
                sub_t = int(sub.post_date.timestamp())
                sub_dt = datetime.fromtimestamp(sub_t).strftime('%I:%M:%S %p, %a, %b %d, %Y')
                sub_dict = dict(user=sub.user.name, image=sub.user.image, content=sub.content, post_date=sub_dt, id=sub.id)
                subcomment.append(sub_dict)
            c_dict.update(subcomment=subcomment)
        result.append(c_dict)
    return JsonResponse(dict(comments=result))
    
    
def api_subcomment(request, auto_id, comment_id):
    
    '''
    post a new subcomment
    '''
    
    if request.method == 'POST':
        if not request.get_user:
            return HttpResponse('Please sign in', status=403)
        content = request.POST.get('content', '').lstrip('\n').rstrip()
        if not content:
            return HttpResponse('Content cannot be empty.', status=403)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.subcomment_set.create(user_id=request.get_user.id, content=content, post_date=timezone.now())
    return HttpResponseRedirect(reverse('weblog:api_blog_comment', args=(auto_id,)))


def delete(request, key, id):
    
    '''
    delete something from database
    '''
    
    if request.get_user and request.get_user.admin:
        if request.method == 'POST':
            if key == 'comments':
                comment = get_object_or_404(Comment, pk=id)
                auto_id = comment.blog.auto_id
                comment.delete()
            elif key == 'subcomments':
                subcomment = get_object_or_404(Subcomment, pk=id)
                auto_id = subcomment.comment.blog.auto_id
                subcomment.delete()
            else:
                raise Http404('Do not exist')
        return HttpResponseRedirect(reverse('weblog:api_blog_comment', args=(auto_id,)))
    else:
        return HttpResponse('Permission denied', 403)