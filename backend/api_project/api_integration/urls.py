from django.urls import path, include
from . import views, API_call_information

urlpatterns = [
    path('', views.github_user_info, name='github_user_info'), # main page
    path('user', views.github_user_info, name='github_user_info'), #shows info of user
    path('postRequest/',views.process_vue_POST_request,name='process-POST-request'), #URL handle for parsing POST request data 
    path('all/', API_call_information.get_github_information, name = 'all'),
    path('delete/', views.delete_entry_db, name = 'delete'),
    path('deleteAll', views.delete_all_records, name = 'deleteAll'),
    path('package', views.repo_frontend_info, name = 'frontend_info'),
    path('home', views.homepage_datapackage, name = 'homepage_datapackage'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
    