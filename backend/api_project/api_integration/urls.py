from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.github_user_info, name='github_user_info'), # main page
    path('user', views.github_user_info, name='github_user_info'), #shows info of user
    path('repo', views.github_repo_info, name='github_repository_info'), # atm shows pull request for specific repo
    path('repos/<str:owner>/<str:repo>/pulls/<str:pull_number>/comments', views.github_repo_pull_comments, name='github_repo_deployments'),
    path('github-pulls/', views.github_repo_pull_requests, name='github_repo_pull_requests'), #URL for displaying JSON dictionary for github repo PRs API endpoint
    path('testUser/', views.testUser, name='testUser'), #URL for displaying testUser function.
]
