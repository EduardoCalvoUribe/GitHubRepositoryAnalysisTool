from django.shortcuts import render
import requests
from django.conf import settings
from django.http import JsonResponse

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