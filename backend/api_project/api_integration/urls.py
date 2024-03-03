from django.urls import path
from . import views

urlpatterns = [
    path('user', views.github_user_info, name='github_user_info'),
    path('repos/<str:owner>/<str:repo>/pulls/<str:pull_number>/comments', views.github_repo_pull_comments, name='github_repo_deployments'),
    path('github-pulls/', views.github_repo_pull_requests, name='github_repo_pull_requests'),
    path('keys/', views.formatted_JSON, name='formatted_JSON'),
    path('dump/', views.dumpUser, name='dumpUser'),
]
