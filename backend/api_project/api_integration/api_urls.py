from django.urls import path, include
from . import views, functions, commit_info

urlpatterns = [
    path("user_vars/", views.load_users, name="item-list"), #for listing all users we can send to the frontend, might delete it later
    path("repo_vars/", views.load_repos, name="item-list"), #for listing all repos we can send to the frontend
    path('quantify',functions.pull_request_per_user, name='request-per-user'),
    path('commits/<str:owner>/<str:repo>/<str:start_date>/<str:end_date>/<str:status>/<str:set>', commit_info.repo_total_commits, {'pull_number': None}, name='total_commits'), # To get all information from commits over branches and pull requests
    path('commits/<str:owner>/<str:repo>/<str:pull_number>', commit_info.repo_total_commits, {'start_date': None, 'end_date': None, 'status': None, 'set': None}, name='get_pull_commits'), # To get all information of commits from a certain pull request
]