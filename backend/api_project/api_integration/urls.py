from django.urls import path
from . import views
from .views import ItemListCreateView

urlpatterns = [
    path('user', views.github_user_info, name='github_user_info'),
    path('repos/<str:owner>/<str:repo>/pulls/<str:pull_number>/comments', views.github_repo_pull_comments, name='github_repo_deployments'),
    path('github-pulls/', views.github_repo_pull_requests, name='github_repo_pull_requests'), #URL for displaying JSON dictionary for github repo PRs API endpoint
    path('testUser/', views.testUser, name='testUser'), #URL for displaying testUser function. 
    path('items/', ItemListCreateView.as_view(), name='item-list-create'), #for listing all items we can send to the frontend
]
