from django.contrib import admin

from weblog.models import User, Blog, Comment, Subcomment

admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Subcomment)