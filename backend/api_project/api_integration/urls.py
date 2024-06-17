from django.urls import path, include
from . import views, API_call_information

urlpatterns = [
    path('', views.github_user_info, name='github_user_info'), # main page
    path('postRequest/',views.process_vue_POST_request,name='process-POST-request'), #URL handle for parsing POST request data 
    path('all/', API_call_information.get_github_information, name = 'all'), # Path called to add a repository to the database
    path('delete/', views.delete_entry_db, name = 'delete'), # Path called to delete a certain repo from the databse
    path('deleteAll', views.delete_all_records, name = 'deleteAll'), # Path called to delete everything from the database (backend)
    path('package', views.repo_frontend_info, name = 'frontend_info'), # Path called to send package of repo info to the frontend
    path('home', views.homepage_datapackage, name = 'homepage_datapackage'), # Path called to send package for home page frontend
    path('login/', views.login_view, name='login'), # Path for login page
]
    