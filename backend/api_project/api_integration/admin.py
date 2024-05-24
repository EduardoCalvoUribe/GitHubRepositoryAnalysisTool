from django.contrib import admin
from .models import Users, Repos, Commit, PullRequest, Comment

# Register your models here.
admin.site.register(Users)
admin.site.register(Repos)
admin.site.register(Commit)
admin.site.register(Comment)
admin.site.register(PullRequest)