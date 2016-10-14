import time, hashlib

from django.db import models


class User(models.Model):
    name = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    created = models.DateTimeField('date created')
    admin = models.BooleanField(default=False)
    image = models.CharField(max_length=200, default='/weblog/img/user.png')
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        sha1_password = self.password + self.email + 'the-Salt'
        self.password = hashlib.sha1(sha1_password.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)


class Blog(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    tag = models.CharField(max_length=50)
    content = models.TextField()
    post_date = models.DateTimeField()
    last_modified = models.DateTimeField(default=None)
    
    def __str__(self):
        return self.title
    
    def summary(self):
        return self.content[:140]
    
    
class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    content = models.TextField()
    post_date = models.DateTimeField()
    
    def __str__(self):
        return self.content[:8]
    

class Subcomment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    content = models.TextField()
    post_date = models.DateTimeField()
    
    def __str__(self):
        return self.content[:8]