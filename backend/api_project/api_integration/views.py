from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth import logout, authenticate
from django.conf import settings
import requests, json, re
from .models import Repository, PullRequest, Commit, User, Comment
from . import functions, API_call_information, general_semantic_score
from rest_framework.authtoken.models import Token
from dateutil.parser import parse
from datetime import datetime
from collections import OrderedDict
from .nlp_functions.AsyncCodeCommitMessageRatio import compute_code_commit_ratio

def github_user_info(request):
    json_response = functions.get_api_reponse('https://api.github.com/user').json()
    return JsonResponse(json_response)
   
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

    return url

@csrf_exempt
def delete_entry_db(request):
    try:
        print("Delete entry")
        # Extract id from POST request
        id = process_vue_POST_request(request)
        # Delete repodata corresponding to id from database
        repository = Repository.objects.get(id=id)
        delete_repository_references(request, repository)
        repository.delete()
        return homepage_datapackage(request)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def delete_repository_references(request, repository):
    try:
        for pull in repository.pull_requests_list:
            PullRequest.objects.filter(url=pull).delete()
        for commit in repository.commits_list:
            Commit.objects.filter(url=commit).delete()
        for comment in repository.comments_list:
            Comment.objects.filter(url=comment).delete()
        for user in repository.users_list:
            User.objects.filter(login=user).delete()
        return True
    except Exception as e:
        return False

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

@csrf_exempt
def send_post_request_to_repo_frontend_info(request):
    try:
        # Create a mock request object
        mock_request = HttpRequest()
        mock_request.method = 'POST'
        
        # Call the repo_frontend_info function with the mock request object
        response = repo_frontend_info(mock_request)
        
        # Return the response
        return response

    except Exception as e:
        # If an exception occurs, return an error response
        return JsonResponse({"error": str(e)}, status=500)

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
            url = data['url']
            dates = data['date']
            ranged = False
            if dates != "homepage" and dates != None:
                print(dates)
                ranged = True
                begin_date, end_date = date_range(dates)
        except json.JSONDecodeError:
            print("Error")
    try:
    # Get the repository by URL (using get() for single object retrieval)
        repo = Repository.objects.get(url=url)
    except Repository.DoesNotExist:
    # Handle repository not found (e.g., return a not found response)
        return JsonResponse({'error': 'Repository not found'}, status=404)

    try:
        # Prepare the response data with nested pull request details
        # Initialize total commit and comment counts
        total_commit_count = 0
        total_comment_count = 0

        # Prepare the response data with nested pull request details
        data = {
            "Repo": {
                "name": repo.name,
                "url": repo.url,
                "updated_at": repo.updated_at,
                "pull_requests": [],
                "number_pulls": 0,
                "total_commit_count": 0,
                "total_comment_count": 0,
                "average_semantic": 0,
                # engagement_score: 0,
            }
        }
        
        pull_requests = repo.pull_requests.all()
        for pr in pull_requests:
            if not ranged:
                data, total_comment_count, total_commit_count = selected_data(pr,data, total_comment_count, total_commit_count,begin_date=None,end_date=None, ranged=False)
            else:
                if (pr.closed_at > begin_date) & (pr.date < end_date) & (pr.date > begin_date):
                    data, total_comment_count,total_commit_count = selected_data(pr,data, total_comment_count, total_commit_count, begin_date, end_date, ranged=True)
        return JsonResponse(data)
    except Repository.DoesNotExist:
        return JsonResponse({"error": "Repository not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def selected_data(pr,data, total_comment_count, total_commit_count, begin_date, end_date, ranged):
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
                    "number_commits": 0,
                    "number_comments": 0,
                    "average_semantic": 0,
                    "pr_title_semantic": calculate_pr_semantic(pr.title),
                    "pr_body_semantic": calculate_pr_semantic(pr.body)
    }
    pr_data, total_comment_count = select_comments(pr, pr_data, total_comment_count, begin_date, end_date, ranged)
    pr_data, total_commit_count = select_commits(pr, pr_data, total_commit_count, begin_date, end_date, ranged)

    pr_data["average_semantic"] = calculate_average_semantic_pull(pr_data)
    data["Repo"]["pull_requests"].append(pr_data)
    data["Repo"]["number_pulls"] = len(data["Repo"]["pull_requests"])
    data["Repo"]["total_commit_count"] = total_commit_count
    data["Repo"]["total_comment_count"] = total_comment_count
    data["Repo"]["average_semantic"] = calculate_average_semantic_repo(data["Repo"])
    return data, total_comment_count, total_commit_count

def date_range(data):
    begin_date_str = data[0]
    end_date_str = data[1]
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ" # Assuming format with optional space

    # Parse the datetime string
    begin_date_obj = datetime.strptime(begin_date_str, date_format)
    begin_date_obj = parse(begin_date_obj.strftime("%Y-%m-%d %H:%M:%S"))

    end_date_obj = datetime.strptime(end_date_str, date_format)
    end_date_obj = parse(end_date_obj.strftime("%Y-%m-%d %H:%M:%S"))
    return begin_date_obj, end_date_obj
        
def select_commits(pr, pr_data, total_commit_count, begin_date, end_date, ranged):
    commit_ids = [comment["commit_id"] for comment in pr_data["comments"]]
    for commit in pr.commits.all():
        # Extract the commit_id from the commit URL
        commit_id = parse_Github_url_variables(commit.url)[-1]
        if not ranged or ((commit_id in commit_ids) or ((commit.date < end_date) & (commit.date > begin_date))):
            commit_data = {
                "name": commit.name,
                "url": commit.url,
                "title": commit.title,
                "user": commit.user,
                "date": commit.date,
                "semantic_score": commit.semantic_score,
                "updated_at": commit.updated_at,
            }
            pr_data["commits"].append(commit_data)
            total_commit_count += 1
                
    pr_data["number_commits"] = len(pr_data["commits"])
    return pr_data, total_commit_count

def select_comments(pr, pr_data, total_comment_count, begin_date, end_date, ranged):
    for comment in pr.comments.all():
                    if not ranged or ((comment.date < end_date) & (comment.date > begin_date)):
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
                        total_comment_count += 1
                
    pr_data["number_comments"] = len(pr_data["comments"])
    return pr_data, total_comment_count

#Create a data package that is used by the frontend to show on the frontend
def homepage_datapackage(request):
    # try:
        #We import all the repositories from the database
    repos = Repository.objects.all()
        # We get an ordered dictionary based on unique URLs as keys and name, updated_at as values
    unique_repos = list(OrderedDict((repo.id, {
            "name": repo.name,
            "id": repo.id,
            "url": repo.url,
            "updated_at": repo.updated_at,
            "average_semantic": API_call_information.calculate_semantic_score_repo(repo)
        }) for repo in repos).values())

        # The Repos is a list that has name & updated_at as values
    data = {"Repos" : unique_repos}
    return JsonResponse(data)
    
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
  
def calculate_average_semantic_pull(pr_data):
    total_semantic = 0
    comment_count = 0
    for commit in pr_data["commits"]:
        total_semantic += commit['semantic_score']
    for comment in pr_data["comments"]:
        if comment["comment_type"] == "comment":
            total_semantic += comment['semantic_score']
            comment_count += 1

    total_semantic+=pr_data["pr_title_semantic"]
    total_semantic+=pr_data["pr_body_semantic"]

    total_count = len(pr_data["commits"]) + comment_count + 2 
    # Divison by 0 handled 
    return total_semantic / total_count if total_count > 0 else 0 

def calculate_average_semantic_repo(repo_data):
    total_semantic = 0
    for pr in repo_data["pull_requests"]:
        total_semantic += pr['average_semantic']

    # Divison by 0 handled
    return total_semantic / len(repo_data["pull_requests"]) if len(repo_data["pull_requests"]) > 0 else 0  # Prevent division by zero
        
@csrf_exempt
def login_view(request):
    print("received login request")
    data = json.loads(request.body)
    username =  data.get("username")
    password = data.get("password")
    email = data.get("email")
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        response = JsonResponse({'token': token.key})
        response.set_cookie('auth_token', token, httponly=True)
        return response
    else:
        return JsonResponse({'error': False}, status=400)

@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('/login/')  # Redirect to login page after logout

# Helper function which calculates the semantic score for the PR title and body
# It simply encapsulates the same function which is used for the comment semantic score.
# Possibly move this to general_semantic_score.py if metric weights will be passed from frontend
def calculate_pr_semantic(message):
    return general_semantic_score.calculateWeightedCommentSemanticScore(message,0.5,0.5)
