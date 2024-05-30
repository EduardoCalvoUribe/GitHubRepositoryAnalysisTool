from django.contrib import admin
from .models import User, Repository, Commit, PullRequest, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Repository)
admin.site.register(Commit)
admin.site.register(Comment)
admin.site.register(PullRequest)