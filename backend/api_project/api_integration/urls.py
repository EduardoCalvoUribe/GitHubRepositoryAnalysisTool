from django.urls import path, include
from . import views, comment_info, API_call_information


# importing nlp_functions to test function output on webpage. 
from .nlp_functions import FleschReadingEase


urlpatterns = [
    path('', views.github_user_info, name='github_user_info'), # main page
    path('user', views.github_user_info, name='github_user_info'), #shows info of user
    path('repo', views.github_repo_info, name='github_repository_info'), # atm shows pull request for specific repo
    path('repos/<str:owner>/<str:repo>/pulls/<str:pull_number>/comments', views.github_repo_pull_comments, name='github_repo_deployments'),
    path('github-pulls/', views.github_repo_pull_requests, name='github_repo_pull_requests'), #URL for displaying JSON dictionary for github repo PRs API endpoint
    path('testUser/', views.testUser, name='testUser'), #URL for displaying testUser function. 
    #path('items/', ItemListCreateView.as_view(), name='item-list-create'), #for listing all items we can send to the frontend
    path('postRequest/',views.process_vue_POST_request,name='process-POST-request'), #URL handle for parsing POST request data 
    path('nlp/',FleschReadingEase.calculate_flesch_reading_ease,name='nlp'), #URL handle for parsing POST request data
    path('comments/', comment_info.comment_visual, name ='comments'),
    path('all/', API_call_information.get_github_information, name = 'all') 
]
