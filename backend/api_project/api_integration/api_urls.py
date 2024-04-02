from django.urls import path, include
from . import views, functions

urlpatterns = [
    path("user_vars/", views.load_users, name="item-list"), #for listing all users we can send to the frontend, might delete it later
    path("repo_vars/", views.load_repos, name="item-list"), #for listing all repos we can send to the frontend
    path('quantify',functions.pull_request_per_user, name='request-per-user')
]