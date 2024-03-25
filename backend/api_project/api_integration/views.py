from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import requests
# import json
from django.conf import settings
from django.http import JsonResponse
from rest_framework import generics
from .models import Users
from .models import Repos
# from .serializers import ItemSerializer

# TO ADD: list of relevant API endpoints as a Python list/enum.

# API call to https://api.github.com/user endpoint
def github_user_info(request):
    json_response = get_api_reponse('https://api.github.com/user').json()
    Users.save_user_to_db(json_response)
    return JsonResponse(json_response)

# API call to https://api.github.com/user endpoint
def github_repo_info(request):
    api_url = f"https://api.github.com/repos/plausible/analytics"

    try:
        api_response = get_api_reponse(api_url)
        pull_requests = api_response.json()
        Repos.save_repo_to_db(pull_requests)
        return JsonResponse({'pull_requests': pull_requests})

    except requests.RequestException as e:
        return JsonResponse({'error': str(e)})

# API call to endpoint with variables in endpoint URL. ATTENTION: Does not work properly yet. 
def github_repo_pull_comments(request, owner, repo, pull_number):
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/comments'
    api_response = get_api_reponse(url)

    # Check if the request was successful
    if api_response.status_code == 200:
        # Convert the response content to JSON and return
        return JsonResponse(api_response.json(), safe=False)
    else:
        # If the request was not successful, return an empty dictionary
        return JsonResponse({}, status=api_response.status_code)
    

def get_api_reponse(URL):
    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    headers = {'Authorization': f'token {personal_access_token}'}
    api_response = requests.get(URL, headers=headers)

    return api_response
     

# API call to https://api.github.com/repos/django/django/pulls endpoint. 
# TO ADD: Repos as variable
def github_repo_pull_requests(request):
    # API call authorisation
    url = 'https://api.github.com/repos/django/django/pulls'
    # Make the GET request to the GitHub API
    api_response = get_api_reponse(url)

    # Check if the request was successful
    if api_response.status_code == 200:
        # Return the JSON data as Django JsonResponse.         
        return JsonResponse(api_response.json(),safe=False)
    else:
        # If the request was unsuccessful, print the error message
        print(f"Failed to fetch data from GitHub API: {api_response.status_code} - {api_response.text}")
        return None
    
# This function accepts an API response for a given API endpoint "URL", 
# and creates a Django HttpResponse (displays key/value pairs)
def handle_API_request(request,URL):
    # API call
    api_response = get_api_reponse(URL)


    json_response = api_response.json()

    # Variable which collects dictionary into string.
    text_to_display = ""

    # json_response.items() is the API response in JSON format converted to a dictionary.
    # For conversion from dictionary to dataframe, see URL 
    # https://stackoverflow.com/questions/13575090/construct-pandas-dataframe-from-items-in-nested-dictionary 
    for key,value in json_response.items():
        # For every key/value pair in dictionary, creates HTTP formatted string.
        text_to_display += "<p><b>"+str(key) + "</b>: " + str(value) + "</p>"

    # Return text_to_display in Django HttpResponse format (in order to display on URL)
    return HttpResponse(text_to_display)




# This function is an example call of handle_API_request for API endpoint https://api.github.com/user.
def testUser(request):   
    return handle_API_request(request,'https://api.github.com/user')
    
# list all save users
def load_users(request):
        data = list(Users.objects.values())
        return JsonResponse({'users': data})

# list all saved repositories
def load_repos(request):
        data = list(Repos.objects.values())
        return JsonResponse({'repositories': data})
    

def pull_request_per_user(request):
    url = 'https://api.github.com/repos/django/django/pulls'
    # Make the GET request to the GitHub API
    api_response = get_api_reponse(url).json()
    id_counts = {}  # Dictionary to store the counts for each 'id'

    # Iterate over each item in the API response
    for item in api_response:
        user_id = item.get('user', {}).get('id')  # Get the 'id' value from the dictionary
        user_login = item.get('user', {}).get('login')  # Get the 'login' value from the dictionary
        key = "{}({})".format(user_id,user_login)
        if user_id:
            id_counts[key] = id_counts.get(key, 0) + 1  # Increment the count for the 'id'

    sorted_user_count_dict = dict(sorted(id_counts.items(), key=lambda x: x[1], reverse=True)) # create a sorted by value dictionary of the user_id's
    print(sorted_user_count_dict)

    return JsonResponse({'repositories': sorted_user_count_dict})