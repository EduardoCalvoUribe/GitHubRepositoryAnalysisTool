from django.urls import path, include
from . import views

urlpatterns = [
    path("user_vars/", views.load_users, name="item-list"), #for listing all items we can send to the frontend
    path("repo_vars/", views.load_repos, name="item-list"), #for listing all items we can send to the frontend
]
