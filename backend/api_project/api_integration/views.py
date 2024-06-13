from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize
from django.utils import timezone
import numpy as np
import requests
import json
import re
from django.conf import settings
from django.http import JsonResponse
from rest_framework import generics
from .models import Repository, PullRequest, Commit, User
from . import functions, API_call_information
# from .serializers import ItemSerializer
from django.views.decorators.csrf import csrf_exempt
import aiohttp
import asyncio
from django.http import JsonResponse
from .models import Comment
from datetime import datetime
from collections import OrderedDict

# # Helper function which loads in the JSON response from
# # the github_repo_pull_requests function and counts the number of pull requests for a given repo. 
# def pull_request_count(request):
#     url = "https://api.github.com/repos/lucidrains/PaLM-rlhf-pytorch/pulls"
#     response = github_repo_pull_requests(request, url)
    
#     if response.status_code == 200:
#         # Deserialize the JSON content
#         pr_data = json.loads(response.content)
#         pr_count = len(pr_data)
        
#         # Create a dictionary containing the PR count
#         data = {"pr_count": pr_count}
        
#         # Return a JSON response with the PR count
#         return JsonResponse(data)
#     else:
#         # Directly return the error response
#         return response

# # Function which creates a package containing the PR count for the url specified in pull_request_count
# # NOTE: URL parsing should still be implemented in pull_request_count, but the function does exist somewhere in project already
# # This function can be used to print pr_count on Django web page
# def pr_count_JSON(request):
#     pr_count = pull_request_count(request)
    
#     # Create JSON package containing the comment count
#     try:
#         # Add comment count to JSON data
#         data = {
#             "pr_count": pr_count
#         } 
#         # 
#         return HttpResponse(json.dumps(data), content_type='application/json')
#     except Exception as e:
#         error_data = {"error": str(e)}
#         return HttpResponse(json.dumps(error_data), content_type='application/json', status=500)
        
# API call to https://api.github.com/user endpoint
def github_user_info(request):
    json_response = functions.get_api_reponse('https://api.github.com/user').json()
    User.save_user_to_db(json_response)
    return JsonResponse(json_response)

# API call to https://api.github.com/user endpoint
def github_repo_info(request):
    api_url = f"https://api.github.com/repos/plausible/analytics"

    try:
        api_response = functions.get_api_reponse(api_url)
        pull_requests = api_response.json()
        Repository.save_repo_to_db(pull_requests)
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
        api_data = api_response.json()
        # Return the JSON data as Django JsonResponse.         
        return JsonResponse(api_response,safe=False)
    else:
        # If the request was unsuccessful, print the error message
        error_data = {
            "error": f"Failed to fetch data from GitHub API: {api_response.status_code} - {api_response.text}"
        }
        return JsonResponse(error_data, status=api_response.status_code)
    
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

    return "https://github.com/lucidrains/PaLM-rlhf-pytorch"

# Simple rapper function which can display POST request Github API URL on Django website
def display_POST_request(request):
    url = process_vue_POST_request(request)
    return HttpResponse(url)

# This function is an example call of handle_API_request for API endpoint https://api.github.com/user.
def testUser(request):   
    return handle_API_request(request,'https://api.github.com/user')
    
# list all save users
def load_users(request):
        data = list(User.objects.values())
        return JsonResponse({'users': data})

# list all saved repositories
def load_repos(request):
        data = list(Repository.objects.values())
        return JsonResponse({'repositories': data})
    

def load_quantify_users(request):
     data = functions.pull_request_per_user(request) # get amount of pull request per user
     return JsonResponse({'repositories': data})


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

    # Extract names from each instance
    names = [pull_request.title for pull_request in pull_requests]

    # Print or use the names as needed
    names = ["test1", "test2"]
    return JsonResponse({'names': names}, safe=False)

@csrf_exempt
def delete_entry_db(request):
    # extract id from POST request
    id = process_vue_POST_request(request)
    # delete repodata corresponding to id from database
    repository = Repository.objects.filter(id=id)
    repository.delete()
    
    
    return JsonResponse(id, safe=False)


def save_comment_view(request):
    # Example data for creating a Comment instance
    comment_response = {
        'comment': {
            'url': 'http://example.com/comment/1',
            'author': {'date': '2024-05-24'}
        },
        'body': 'This is a comment',
        'user': {'login': 'testuser'}
    }
    semantic_score = 0.85

    # Create and save the Comment instance
    comment = Comment(
        url=comment_response['comment']['url'],
        date=comment_response['comment']['author']['date'],
        body=comment_response['body'],
        user=comment_response['user']['login'],
        semantic_score=semantic_score
    )
    comment.save()

    # Retrieve all Comment instances from the database
    data = list(Comment.objects.values())
    return JsonResponse({'data': data})

# Function to delete all items from database
def delete_all_records(request):
    try:
        User.objects.all().delete()
        Repository.objects.all().delete()
        PullRequest.objects.all().delete()
        Commit.objects.all().delete()
        Comment.objects.all().delete()
        return True, "All records deleted successfully."
    except Exception as e:
        return False, str(e)

# Function to send a package of all repo information to the frontend
@csrf_exempt
def repo_frontend_info(request):
    if request.method == 'POST':
        # Get the request body as a string
        request_body = request.body.decode('utf-8')
        # Try to parse the JSON data
        try:
            # Option 1: Using a dictionary (recommended)
            data = json.loads(request_body)
            #url = data.get('url')  # Use get() for optional retrieval
            url = data['url']
            print("url reached")
            dates = data['date']
            begin_date, end_date = date_range(dates)
        except json.JSONDecodeError:
            print("Error")
    print("Point reached")
    url = "https://github.com/lucidrains/PaLM-rlhf-pytorch"
    begin_date = timezone.make_aware(datetime(2024, 3, 1, 0, 0, 0))
    end_date = timezone.make_aware(datetime(2024, 6, 1, 0, 0, 0))
    print(url)
    try:
    # Get the repository by URL (using get() for single object retrieval)
        repo = Repository.objects.get(url=url)
    except Repository.DoesNotExist:
    # Handle repository not found (e.g., return a not found response)
        return JsonResponse({'error': 'Repository not found'}, status=404)

    try:
            # Prepare the response data with nested pull request details
        data = {
            "Repo": {
            "name": repo.name,
            "url": repo.url,
            "updated_at": repo.updated_at,
            "pull_requests": [],
            }
        }

        pull_requests = repo.pull_requests.all()
        print("Getting data reached")
        print(pull_requests)
        print("But really")
        for pr in pull_requests:
            print("In for loop")
            print(type(pr.date))
            print("in between pr.date and begin_date")
            print(type(begin_date))
            print(f"Date: {pr.date}")
            # if pr.date != None:
            print("pr.date not None")
            if (pr.closed_at > begin_date) & (pr.date < end_date) & (pr.date > begin_date):
                    print("Data if reached")
                    pr_data = {
                    "url": pr.url,
                    "updated_at": pr.updated_at,
                    "date": pr.date,
                    "title": pr.title,
                    "body": pr.body,
                    "user": pr.user,
                    "number": pr.number,
                    "closed_at": pr.closed_at,
                    "commits": [],
                    "comments": [],
                    }

                    pr_data["commits"].append(select_commit(pr))

                    for comment in pr.comments.all():
                        comment_data = {
                            "url": comment.url,
                            "date": comment.date,
                            "body": comment.body,
                            "user": comment.user,
                            "semantic_score": comment.semantic_score,
                            "updated_at": comment.updated_at,
                            "comment_type": comment.comment_type,
                            "commit_id": comment.commit_id,
                        }
                        pr_data["comments"].append(comment_data)

            data["Repo"]["pull_requests"].append(pr_data)
        return JsonResponse(data)
    except Repository.DoesNotExist:
        return JsonResponse({"error": "Repository not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def date_range(data):
    try:
        begin_date_str = data.get('0')
        end_date_str = data.get('1')
        print("daterange 1")
        date_format = '%a %b %d %Y %H:%M:%S GMT%z (%Z)'
        print("daterange 2")
        begin_date_obj = timezone.make_aware(datetime.strptime(begin_date_str, date_format))
        end_date_obj = timezone.make_aware(datetime.strptime(end_date_str, date_format))
        print("daterange 3")
    except:
        return ""
    return begin_date_obj, end_date_obj

def select_commit(pull_request):
    for commit in pr.commits.all():
                commit_data = {
                    "name": commit.name,
                    "url": commit.url,
                    "title": commit.title,
                    "user": commit.user,
                    "date": commit.date,
                    "semantic_score": commit.semantic_score,
                    "updated_at": commit.updated_at,
                }
    return commit_data

#Create a data package that is used by the frontend to show on the frontend
def homepage_datapackage(request):
    print("Homepage reached")
    #try:
        #We import all the repositories from the database
    repos = Repository.objects.all()
    print(repos)
        # We get an ordered dictionary based on unique URLs as keys and name, updated_at as values
    unique_repos = list(OrderedDict((repo.id, {
            "name": repo.name,
            "id": repo.id,
            "url": repo.url,
            "updated_at": repo.updated_at,
        }) for repo in repos).values())

        # The Repos is a list that has name & updated_at as values
    data = {"Repos" : unique_repos}
    return JsonResponse(data)
    # except Repository.DoesNotExist:
    #     return JsonResponse({"error": "Repository not found"}, status=404)
    
# def engagement_score(request):
#     # The calculation is based on the type(s) of object(s) you'd like to calculate the engagement score of
#     user, repository = process_vue_POST_request(request)['user'], process_vue_POST_request(request)['repository']
#     if user is User & repository is Repository:
#         # User for specific repo
#         total_comments, total, commits, total_pull_request = 
#         print("User engagement score for specific repo")
#     elif user is User:
#         # user specific score
#         total_comments, total, commits, total_pull_request = user.comments., User.commits.all(), User.pull_requests.all()

#         print("User engagement score for all repo's")
#     elif repository is Repository:
#         total_comments, total, commits, total_pull_request = 
#         print("Repository engagement score")

    # return total_comments, total, commits, total_pull_request, engagement_score

async def comment_test(request):
    owner = "IntersectMBO"
    repo = "plutus"
    pull_number = "4733"

    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    # Headers for the API request
    headers = {'Authorization': f'token {personal_access_token}'}
    async with aiohttp.ClientSession(headers=headers) as session:
        pr_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}"
        async with session.get(pr_url) as response:
            # Convert the response in a JSON response
            pull_request = await response.json()
            comments = await API_call_information.fetch_comments(session, pull_request)
            comment_counter = 0
            for comment in comments:
                comment_counter += 1
        
        return JsonResponse(str(comment_counter), safe=False)
    
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

  return parsed_url
  
  if parsed_url[0] != 'github.com':
    return ['URL is not a Github URL']
  else:
    return parsed_url