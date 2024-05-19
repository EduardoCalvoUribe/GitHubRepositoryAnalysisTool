from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import requests
import json
import re
from django.conf import settings
from django.http import JsonResponse
from rest_framework import generics
from .models import Users
from .models import Repos, PullRequest, Commit
from . import functions
# from .serializers import ItemSerializer
from django.views.decorators.csrf import csrf_exempt

# TO ADD: list of relevant API endpoints as a Python list/enum.

# API call to https://api.github.com/user endpoint
def github_user_info(request):
    json_response = functions.get_api_reponse('https://api.github.com/user').json()
    Users.save_user_to_db(json_response)
    return JsonResponse(json_response)

# API call to https://api.github.com/user endpoint
def github_repo_info(request):
    api_url = f"https://api.github.com/repos/plausible/analytics"

    try:
        api_response = functions.get_api_reponse(api_url)
        pull_requests = api_response.json()
        Repos.save_repo_to_db(pull_requests)
        return JsonResponse({'pull_requests': pull_requests})

    except requests.RequestException as e:
        return JsonResponse({'error': str(e)})

# API call to endpoint with variables in endpoint URL. ATTENTION: Does not work properly yet. 
def github_repo_pull_comments(request, owner, repo, pull_number):
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/comments'
    api_response = functions.get_api_reponse(url)

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
    api_response = functions.get_api_reponse(url)

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
    api_response = functions.get_api_reponse(URL)


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

    return str(url)

# Simple rapper function which can display POST request Github API URL on Django website
def display_POST_request(request):
    url = process_vue_POST_request(request)
    return HttpResponse(url)




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
    

def load_quantify_users(request):
     data = functions.pull_request_per_user(request) # get amount of pull request per user
     return JsonResponse({'repositories': data})

# Helper function that parses Github URLs into a list of variables
# Assuming that Github URLs always follow the same pattern, i.e. https://gihtub.com/[username]/[repo_name]/etc...
# Returns a list of variables if the provided URL was a Github URL
def parse_Github_url_variables(url):
  # Indicate empty URL if url is empty
  if not url:
    return ['empty URL']

  # Filter out www, http and https from URL
  filtered_url = re.sub(r'https?://(www\.)?', '', url)
  parsed_url = filtered_url.split('/')

  
  if parsed_url[0] != 'github.com':
    return ['URL is not a Github URL']
  else:
    return parsed_url

# Function which accepts list of Github variables and returns a dictionary containing
# all variables contained in the parsed URL. 
def assign_Github_variables(parsed_url):
  variable_dictionary = {
      "username":"",
      "repo_name":"",
      "pull_number":"",
      "nested_commit":"",
      "nested_commit_sha":"",
  }

  # Assign username to variable_dictionary (if available)
  if len(parsed_url) > 1:
        variable_dictionary["username"] = parsed_url[1]
  # Assign repo_name to variable_dictionary (if available)
  if len(parsed_url) > 2:
        variable_dictionary["repo_name"] = parsed_url[2]
  # Assign pull_number to variable_dictionary (if available)
  if len(parsed_url) > 3 and parsed_url[3] == 'pull':
        variable_dictionary["pull_number"] = parsed_url[4] if len(parsed_url) > 4 else ""
  # Assign nested_commit and nested_commit_sha to variable_dictionary (if available)
  if len(parsed_url) > 5 and parsed_url[3] == 'pull' and parsed_url[5] == 'commits':
        variable_dictionary["nested_commit"] = parsed_url[5]
        variable_dictionary["nested_commit_sha"] = parsed_url[6] if len(parsed_url) > 6 else ""


@csrf_exempt
def frontendInfo(request):
    # Retrieve all instances of PullRequest model
    pull_requests = Commit.objects.all()
    print(pull_requests)

    # Extract names from each instance
    names = [pull_request.title for pull_request in pull_requests]

    # Print or use the names as needed
    print(names)
    names = ["test1", "test2"]
    return JsonResponse({'names': names}, safe=False)

@csrf_exempt
def delete_entry_db(request):
    # extract id from POST request
    id = process_vue_POST_request(request)
    # delete repodata corresponding to id from database
    Repos.objects.filter(id=id).delete()
    return JsonResponse(id, safe=False)