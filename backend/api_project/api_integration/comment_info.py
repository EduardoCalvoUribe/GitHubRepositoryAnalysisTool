# Identical imports to commit_info.py file
from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.conf import settings
from datetime import datetime
from collections import Counter

def comment_visual(response):
    # NOTE: Personal access token with repo permission turned on IS REQUIRED!
    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN

    # Headers for the API request
    headers = {'Authorization': f'token {personal_access_token}'}

    # Testing with open pull request at https://github.com/lucidrains/PaLM-rlhf-pytorch/pull/52
    owner = 'IntersectMBO'
    repo = 'plutus'
    pull_number = 5772

    # Test run to retrieve all comments from https://github.com/lucidrains/PaLM-rlhf-pytorch/pull/52
    all_comments = get_pull_request_comments(owner, repo, pull_number, headers)

    text_to_display = ''

    # Print the textual content of all_comments separated by dashes 
    for comment in all_comments:
        text_to_display += '-----------------</p>'
        text_to_display += f'</b>Type of comment:</b> {comment['comment_type']}</p>'
        if 'body' in comment and comment['body']:  
            text_to_display += comment['body']
        else:
            text_to_display += 'No body'
        text_to_display += "</p>"

    return HttpResponse(text_to_display)



# Function which makes API calls to retrieve all comments for some pull request.

# NOTE: This function sends an API request to two slightly different API endpoints. 
# This does correctly return (almost, see NOTE 2) all comments for a PR, including comments which are reactions to comments.

# TO ADD: take token pagination into account, i.e. check if there are more comments to retrieve with 'next'

# NOTE 2: The first comment (might be the pull request message itself?) doesn't seem to be considered as a comment. 
# Thus first comment is not added to all_comments yet. Look into this!
def get_pull_request_comments(owner, repo, pull_number, headers):
    pr_comments_pulls_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/comments'
    pr_comments_issues_url = f'https://api.github.com/repos/{owner}/{repo}/issues/{pull_number}/comments'
    pr_comments_reviews_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/reviews'

    # Initialise empty list which will store all comments for a PR
    all_comments = []

    # Recursive definition which retrieves all comments for a given URL    
    def retrieve_comments(comment_url, type):
        # Make API request to specified url
        response = requests.get(comment_url, headers=headers)
        # Format response to JSON
        comments = response.json()
        
        # Loop through all comments in JSON response
        for comment in comments:
            comment['comment_type'] = type
            all_comments.append(comment)         


    # NOTE: The following calls to retrieve_comments successfully retrieve all comments for a PR (apart from the very first one.)                                

    # Retrieve comments from the pulls URL
    # This ensures that all comments which are reactions are added to all_comments.            
    retrieve_comments(pr_comments_pulls_url, 'pulls API')

    # Retrieve comments from the reviews URL
    # This ensures that all review comments are added to all_comments.
    retrieve_comments(pr_comments_reviews_url, 'review API')
    
    # Retrieve comments from the issues URL
    # This ensures that all primary comments are added to all_comments.
    retrieve_comments(pr_comments_issues_url, 'issues API')



    # Return list containing all comments
    return all_comments