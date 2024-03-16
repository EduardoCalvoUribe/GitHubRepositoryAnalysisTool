from django.shortcuts import render
from django.http import HttpResponse
import requests
# import json
from django.conf import settings
from django.http import JsonResponse
from rest_framework import generics
from .models import *
from .serializers import ItemSerializer

# TO ADD: list of relevant API endpoints as a Python list/enum.


# class ItemListView(generics.ListAPIView):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer

# API call to https://api.github.com/user endpoint
def github_user_info(request):
    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    headers = {'Authorization': f'token {personal_access_token}'}
    api_response = requests.get('https://api.github.com/user', headers=headers)
    return JsonResponse(api_response.json())

# API call to https://api.github.com/user endpoint
def github_repo_info(request):
    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    repo_owner = "plausible"
    repo_name = "analytics"
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"

    try:
        headers = {'Authorization': f'token {personal_access_token}'}
        api_response = requests.get(api_url, headers=headers)
        pull_requests = api_response.json()

        # Process the pull_requests data as needed
        # For example, extract titles, authors, etc.

        return JsonResponse({'pull_requests': pull_requests})

    except requests.RequestException as e:
        return JsonResponse({'error': str(e)})

# API call to endpoint with variables in endpoint URL. ATTENTION: Does not work properly yet. 
def github_repo_pull_comments(request, owner, repo, pull_number):
    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    headers = {'Authorization': f'token {personal_access_token}'}
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/comments'
    api_response = requests.get(url, headers=headers)

    # Check if the request was successful
    if api_response.status_code == 200:
        # Convert the response content to JSON and return
        return JsonResponse(api_response.json(), safe=False)
    else:
        # If the request was not successful, return an empty dictionary
        return JsonResponse({}, status=api_response.status_code)
    

def get_json_data(URL):
    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    headers = {'Authorization': f'token {personal_access_token}'}
    api_response = requests.get(URL, headers=headers)

    # Convert API response to JSON format
    json_response = api_response.json()
    return json_response

# API call to https://api.github.com/repos/django/django/pulls endpoint. 
# TO ADD: Repos as variable
def github_repo_pull_requests(request):
    # API call authorisation
    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    headers = {'Authorization': f'token {personal_access_token}'}

    url = 'https://api.github.com/repos/django/django/pulls'

    # Make the GET request to the GitHub API
    api_response = requests.get(url, headers=headers)

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
    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    headers = {'Authorization': f'token {personal_access_token}'}
    api_response = requests.get(URL, headers=headers)

   
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
    

def save_user_to_db(request, json_response):
    try:
        # Convert API response to JSON format
        user = Users()

        for key,value in json_response.items():
            if key is not None:
                if value is not None:
                    setattr(user, key, value)
                else:
                   setattr(user, key, "")

        user.save()
        data = list(Users.objects.values())
        return JsonResponse({'data': data})
    except Exception as e:
        return JsonResponse({"error": str(e)})

def save_repo_to_db(request, json_response):
    try:
        # Convert API response to JSON format
        user = Repos()

        for key,value in json_response.items():
            if key is not None:
                if value is not None:
                    setattr(user, key, value)
                else:
                   setattr(user, key, "")

        user.save()
    except Exception as e:
        return JsonResponse({"error": str(e)})



def load_users(request):
        data = list(Users.objects.values())
        return JsonResponse({'data': data})

def load_repos(request):
        data = list(Repos.objects.values())
        return JsonResponse({'data': data})
    
