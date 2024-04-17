# Identical imports to commit_info.py file
from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.conf import settings
from datetime import datetime
from collections import Counter


# NOTE: Personal access token with repo permission turned on IS REQUIRED!
personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN

# Headers for the API request
headers = {'Authorization': f'token {personal_access_token}'}

# Testing with open pull request at https://github.com/lucidrains/PaLM-rlhf-pytorch/pull/52
owner = 'lucidrains'
repo = 'PaLM-rlhf-pytorch'
pull_number = 52



# Function which makes API calls to retrieve all comments for some pull request.

# NOTE: This function sends an API request to two slightly different API endpoints. 
# This does correctly return (almost, see NOTE 2) all comments for a PR, including comments which are reactions to comments.

# TO ADD: take token pagination into account, i.e. check if there are more comments to retrieve with 'next'

# NOTE 2: The first comment (might be the pull request message itself?) doesn't seem to be considered as a comment. 
# Thus first comment is not added to all_comments yet. Look into this!
def get_pull_request_comments(owner, repo, pull_number, headers):
    pr_comments_pulls_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/comments'
    pr_comments_issues_url = f'https://api.github.com/repos/{owner}/{repo}/issues/{pull_number}/comments'

    # Initialise empty list which will store all comments for a PR
    all_comments = []

    # Recursive definition which retrieves all comments for a given URL    
    def retrieve_comments(comment_url):
        # Make API request to specified url
        response = requests.get(comment_url, headers=headers)
        # Format response to JSON
        comments = response.json()

        # Loop through all comments in JSON response
        for comment in comments:
            all_comments.append(comment)

            # Check if the comment has reactions
            if 'reactions' in comment:
                reactions_url = comment['reactions']['url']
                # If comment has reactions recursively retrieve those comments as well.
                retrieve_comments(reactions_url)            


    # NOTE: The following calls to retrieve_comments successfully retrieve all comments for a PR (apart from the very first one.)                                

    # Retrieve comments from the pulls URL
    # This ensures that all comments which are reactions are added to all_comments.            
    retrieve_comments(pr_comments_pulls_url)
    
    # Retrieve comments from the issues URL
    # This ensures that all primary comments are added to all_comments.
    retrieve_comments(pr_comments_issues_url)



    # Return list containing all comments
    return all_comments

# Test run to retrieve all comments from https://github.com/lucidrains/PaLM-rlhf-pytorch/pull/52
all_comments = get_pull_request_comments(owner, repo, pull_number, headers)

# Print the textual content of all_comments separated by dashes 
for comment in all_comments:
    print("----------------------")
    print(comment['body'])
    print(" ")