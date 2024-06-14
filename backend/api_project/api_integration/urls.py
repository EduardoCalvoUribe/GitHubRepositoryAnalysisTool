from django.urls import path, include
from . import views, comment_info, API_call_information, functions, general_semantic_score, commit_info


# importing nlp_functions to test function output on webpage. 
from .nlp_functions import FleschReadingEase


urlpatterns = [
    path('', views.github_user_info, name='github_user_info'), # main page
    path('user', views.github_user_info, name='github_user_info'), #shows info of user
    path('repo', views.github_repo_info, name='github_repository_info'), # atm shows pull request for specific repo
    path('repos/<str:owner>/<str:repo>/pulls/<str:pull_number>/comments', views.github_repo_pull_comments, name='github_repo_deployments'),
    path('github-pulls/<str:url>', views.github_repo_pull_requests, name='github_repo_pull_requests'), #URL for displaying JSON dictionary for github repo PRs API endpoint
    path('testUser/', views.testUser, name='testUser'), #URL for displaying testUser function. 
    #path('items/', ItemListCreateView.as_view(), name='item-list-create'), #for listing all items we can send to the frontend
    path('postRequest/',views.process_vue_POST_request,name='process-POST-request'), #URL handle for parsing POST request data 
    path('nlp/',FleschReadingEase.calculateFleschReadingEase,name='nlp'), #URL handle for parsing POST request data
    path('comments/', comment_info.comment_visual, name ='comments'),
    path('all/', API_call_information.get_github_information, name = 'all'),
    path('database/', views.frontendInfo, name = 'database'),
    path('delete/', views.delete_entry_db, name = 'delete'),
    # path('semantic',general_semantic_score.display_semantic, name = 'semantic'), 
    path('databaseprint/', functions.show_database, name = 'datbaseshow'),
    path('help/',views.save_comment_view, name = 'help'),
    path('deleteAll', views.delete_all_records, name = 'deleteAll'),
    path('package', views.repo_frontend_info, name = 'frontend_info'),
    path('packageRanged', views.repo_frontend_info_dated, name = 'frontend_info_daterange'),
    path('home', views.homepage_datapackage, name = 'homepage_datapackage'),
    path('testCommentJSON/',comment_info.printCommentCountJSON,name = 'testCommentJSON'), #URL for printing combined JSON (comment) package
    path('testCommitJSON/',commit_info.printCommitCountJSON, name = 'testCommitJSON'), #URL for printing JSON commit package
    path('commentTest', views.comment_test, name = 'commentTest'),
    path('testfro', views.send_post_request_to_repo_frontend_info, name = 'testfro'),
    path('testCC', views.testAsyncCodeCommit, name = 'testCC'),
    # path('testPR/',views.pr_count_JSON, name = 'testPR') #URL for printing JSON commit package
    path('login/', views.login_view, name='login'),
    # Optional logout URL pattern
    path('logout/', views.logout_view, name='logout'),
]
    