from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from django.conf import settings
from django.http import JsonResponse
from rest_framework import generics
from .models import Item
from .serializers import ItemSerializer
from django.views.decorators.csrf import csrf_exempt

# TO ADD: list of relevant API endpoints as a Python list/enum.


class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


# API call to https://api.github.com/user endpoint
def github_user_info(request):
    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    headers = {'Authorization': f'token {personal_access_token}'}
    api_response = requests.get('https://api.github.com/user', headers=headers)
    return JsonResponse(api_response.json())

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
    
@csrf_exempt
# API call to https://api.github.com/repos/django/django/pulls endpoint. 
# TO ADD: Repos as variable
def github_repo_pull_requests(request, url):
    # API call authorisation
    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    headers = {'Authorization': f'token {personal_access_token}'}

    # TODO: Extract owner and repo from URL
    # Example Input = 'github.com/repos/IntersectMBO/plutus/pulls'
    # Example Desired Output = 'https://api.github.com/repos/IntersectMBO/plutus'
    # proof of concept:
    # owner = url.split('/')[3]
    # repo = url.split('/')[4]
    # api_response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/pulls', headers=headers)

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

    # Convert API response to JSON format
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
   
@csrf_exempt 
# This function accepts an incoming HTTP request, which is assumed to be a POST request. 
# The function returns a user-requested Github API URL in String form which is extracted from the HTTP request
def process_vue_POST_request(request):
    # If the user request is an HTTP POST request
    if request.method == "POST":
        # Use built-in json Python package to parse JSON string and convert into a Python dictionary
        data = json.loads(request.body)
        
        # Assuming that POST request contains 'url' key and associated value
        url = data.get('url')

    return JsonResponse(str(url), safe=False)

# Simple rapper function which can display POST request Github API URL on Django website
def display_POST_request(request):
    url = process_vue_POST_request(request)
    return HttpResponse(url)


# This function is an example call of handle_API_request for API endpoint https://api.github.com/user.
def testUser(request):   
    return handle_API_request(request,'https://api.github.com/user')
    
# def save_github_repositories_to_db():
#     for repo in github_repositories:
#         GitHubRepository.objects.create(
#             name=repo["name"],
#             description=repo["description"],
#             url=repo["html_url"],
#         )





    
