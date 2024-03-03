from django.shortcuts import render
from django.http import HttpResponse


import requests
from django.conf import settings
from django.http import JsonResponse
# import json
from rest_framework.views import APIView

#note: 
# pip install jsonlib
# pip install djangorestframework
# pip install markdown       # Markdown support for the browsable API.
# pip install django-filter  # Filtering support
from rest_framework import parsers


class github_requests(APIView):
    parser_classes = (parsers.JSONParser,)

    def post(self, request, format=None):
        number = request.data['number']
        requests = request.data['data']


def github_user_info(request):
    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    headers = {'Authorization': f'token {personal_access_token}'}
    api_response = requests.get('https://api.github.com/user', headers=headers)
    return JsonResponse(api_response.json())

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
    

#WORKING FUNCTION! GitHub Repo pull requests API. 
#TO ADD: variable repo name.
def github_repo_pull_requests(request):
    # Construct the URL for the GitHub API endpoint
    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    headers = {'Authorization': f'token {personal_access_token}'}

    url = 'https://api.github.com/repos/django/django/pulls'

    # Make the GET request to the GitHub API
    api_response = requests.get(url, headers=headers)

    # Check if the request was successful
    if api_response.status_code == 200:
        # Return the JSON data
        return JsonResponse(api_response.json(),safe=False)
    else:
        # If the request was unsuccessful, print the error message
        print(f"Failed to fetch data from GitHub API: {api_response.status_code} - {api_response.text}")
        # Return None or raise an exception based on your requirements
        return None
    
def dumpUser(request):   

    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    headers = {'Authorization': f'token {personal_access_token}'}
    api_response = requests.get('https://api.github.com/user', headers=headers)

    json_response = api_response.json()

    text_to_display = ""
    # text_to_display = "The original dictionary is : " + str(api_response.json())

    for key,value in json_response.items():
        text_to_display += "<p>"+str(key) + ":" + str(value) + "</p>"

    return HttpResponse(text_to_display)

    # WORKING TEXT
    # text_to_display = "Hello, this is the text I want to display!"
    # return HttpResponse(text_to_display)






#Function for extracting key-value pairs from JSON data
def extract_outer_keys(data):
    keys = set()
    # If JSON data is formatted as a dictionary
    if isinstance(data, dict):
        for key in data:
            keys.add(key)

    # If JSON data is formatted as a list
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                keys.add(item.keys())    
    return keys

def formatted_JSON(request):
    # JSON response from the GitHub repo pull comments API request
    data = github_repo_pull_requests(request)
    data0 = data[0]['id']
    print(data0)

    return data0
    
    

    #print all keys in data
    # keys = extract_outer_keys(data)
    # print(str(keys))

    # # Convert the set of keys to a list (or perform any other necessary operations)
    # key_list = list(keys)
    # print(key_list)

    # return JsonResponse(urls)     



    
