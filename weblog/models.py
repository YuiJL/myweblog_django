#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

import hashlib, uuid

from django.db import models

from datetime import datetime

class User(models.Model):
    next_id = models.UUIDField(editable=False)
    name = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    created = models.DateTimeField('date created')
    admin = models.BooleanField(default=False)
    image = models.CharField(max_length=200, default='/static/weblog/img/user.png')
    image_cropped = models.CharField(max_length=200, default='/static/weblog/img/user.png')
    
    def __str__(self):
        return self.name
    
    def set_sha1(self):
        sha1_password = self.password + self.email + 'the-Salt'
        self.password = hashlib.sha1(sha1_password.encode('utf-8')).hexdigest()


class Blog(models.Model):
    auto_id = models.IntegerField(default=0)
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    tag = models.CharField(max_length=50)
    content = models.TextField()
    post_date = models.DateTimeField()
    last_modified = models.DateTimeField(auto_now=True)
    new_post = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    def summary(self):
        return self.content[:140]
    
    def save(self, *args, **kw):
        super().save(*args, **kw)
        self.auto_id = self.post_date.year * 10000 + self.id
        super().save(*args, **kw)
    
    
class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    content = models.TextField()
    post_date = models.DateTimeField()
    
    def __str__(self):
        return self.content
    

class Subcomment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    content = models.TextField()
    post_date = models.DateTimeField()
    
    def __str__(self):
        return self.content