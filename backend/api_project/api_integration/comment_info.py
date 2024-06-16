
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from django.conf import settings
from datetime import datetime
from collections import Counter
import aiohttp
import asyncio
from asgiref.sync import sync_to_async
from .models import Comment, PullRequest, Repository
from .general_semantic_score import calculateWeightedCommentSemanticScore
from datetime import datetime
from datetime import date
from django.utils import timezone
from django.db import IntegrityError, transaction
import json

async def comment_visual(response):
    # NOTE: Personal access token with repo permission turned on IS REQUIRED!
    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN

    # Headers for the API request
    headers = {'Authorization': f'token {personal_access_token}'}

    # # Testing with open pull request at https://github.com/lucidrains/PaLM-rlhf-pytorch/pull/52
    # owner = 'lucidrains'
    # repo = 'PaLM-rlhf-pytorch'
    # pull_number = 52


    # Testing with pull request at https://github.com/IntersectMBO/plutus/pull/5772
    # owner = 'IntersectMBO'
    # repo = 'plutus'
    # pull_number = 5772

    #Testing with pull request at https://github.com/RocketChat/Rocket.Chat/pull/7454 (large repo)
    owner = 'RocketChat'
    repo = 'Rocket.Chat'
    pull_number = 7454


    # Ensure PullRequest instance exists
    repository, created = await sync_to_async(Repository.objects.get_or_create)(
        name=repo,  
        owner=owner 
    )
    
    pull_request, created = await sync_to_async(PullRequest.objects.get_or_create)(
        number=pull_number,
        repo=repository  
    )

    
    async with aiohttp.ClientSession(headers=headers) as session: 
        all_comments = await get_pull_request_comments(owner, repo, pull_number, headers)

        text_to_display = ''
        total_amount_comments = 0

        # Print the textual content of all_comments separated by dashes 
        for comment in all_comments:
            text_to_display += '-----------------</p>'
            text_to_display += '<b>Type of comment:</b> '
            # Check if 'comment_type' key exists in the comment dictionary
            if 'comment_type' in comment:
                # Display comment type
                text_to_display += f"{comment['comment_type']}</p>"                
            else:
                # Display N/A if no comment type found
                text_to_display += 'N/A</p>'  
            if 'body' in comment and comment['body']:  
                # Save comment in string format
                comment_text_body = comment['body'] 
                text_to_display += comment_text_body
                                
                # Assign semantic score to the comment            
                # Params of semantic score function are comment, ld weight and fre_weight
                semantic_score = calculateWeightedCommentSemanticScore(comment_text_body, 50, 700)

                # Retrieve data about when comment was created and updated. Converted to YYYY-MM-DD format
                created_at = timezone.make_aware(datetime.strptime(comment.get('created_at', ''), '%Y-%m-%dT%H:%M:%SZ')).date() if comment.get('created_at') else datetime.now()
                updated_at = timezone.make_aware(datetime.strptime(comment.get('updated_at', ''), '%Y-%m-%dT%H:%M:%SZ')) if comment.get('updated_at') else timezone.now()

                comment_type=''
                if 'comment_type' in comment:
                    cmnt_type=comment.get('comment_type','')
                cmt_id=''
                if comment_type == 'review comment':
                    cmt_id=comment.get('commit_id', '')

                try:
                        # Save comment to database asynchronously with database transaction
                        await sync_to_async(transaction.atomic)()

                        # Create a comment instance 
                        comment_instance = Comment(
                            pull_request=pull_request,  # Reference the existing PullRequest instance, foreign key constraint
                            url=comment.get('url', ''), # Get URL of comment
                            date=created_at,  # Date at which comment has been created
                            updated_at=updated_at, # Date at which comment has been updated
                            body=comment_text_body, # Text content of comment
                            user=comment.get('user', {}).get('login', ''), # User associated with comment
                            semantic_score=semantic_score, # Semantic score associated with comment
                            comment_type=cmnt_type,
                            commit_id=cmt_id
                        )

                        # Save comment along with relevant metadata to the database
                        await sync_to_async(comment_instance.save)()
                except IntegrityError as e:
                    # Return error code 400 if saving to database is unsuccessful
                    return JsonResponse({"error": str(e)}, status=400)
                
                total_amount_comments += 1
            else:
                # Display the comment (JSON dictionary) on page if text is not review/issue comment or pull request message
                text_to_display += str(comment)
            text_to_display += "</p>"

        text_to_display = f'</b> Total amount of comments on Pull Request #{pull_number}:</b> {total_amount_comments}</p>' + text_to_display 

        return HttpResponse(text_to_display)
    
# Helper function which uses get_pull_request_comments function to retrieve number of comments
async def get_comment_count(owner,repo,pull_number,headers):
    comment_list = await get_pull_request_comments(owner,repo,pull_number,headers)
    # Return length of comment_list, which corresponds to number of comments
    return len(comment_list)

# Function which creates a package containing the comment count for a given repo, owner, pull_number
# (API) Headers for get_comment_count are defined inside the function
async def comment_count_JSON(owner,repo,pull_number):
    # Token retrieved from settings.py file
    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    # Headers for the API request
    headers = {'Authorization': f'token {personal_access_token}'}

    comment_count = await get_comment_count(owner,repo,pull_number,headers)
    
    # Create JSON package containing the comment count
    try:
        # Add comment count to JSON data
        data = {
            "comment_count": comment_count          
        } 
        # 
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception as e:
        error_data = {"error": str(e)}
        return HttpResponse(json.dumps(error_data), content_type='application/json', status=500)

async def printCommentCountJSON(request):
    owner = 'lucidrains'
    repo = 'PaLM-rlhf-pytorch'
    pull_number = 52
    
    comment_JSON_response = await comment_count_JSON(owner,repo,pull_number)
    # Deserialize JSON from the HttpResponse
    comment_JSON = json.loads(comment_JSON_response.content)
    # Now test python object can be appended
    y = {"year":2024}
    comment_JSON.update(y)

    # Return updated object as JsonResponse. 
    return JsonResponse(comment_JSON)

    
# Function which makes API calls to retrieve all comments for some pull request.
async def get_pull_request_comments(owner, repo, pull_number, session):
    # List of Github API endpoints which are accessed for retrieving all comments associated with a pull request.
    # Note that a distinction exists between review comments and issue comments, both are textual comments which are part of
    # the conversation associated with a pull request, but they are accessed by different endpoints. 
    
    # API endpoint for PR message
    pr_details_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}'
    
    # API endpoint for review comments
    pr_review_comments_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/comments'

    # API endpoint for issue comments
    pr_issue_comments_url = f'https://api.github.com/repos/{owner}/{repo}/issues/{pull_number}/comments'
    
    # Initialise empty list which will store all comments for a PR
    all_comments = []
    tasks = []

    # Recursive asynchronous definition which retrieves all comments for a given URL    
    async def retrieve_comments(comment_url, comment_type, session):
        # While loop which retrieves all comments for a PR WITH token pagination (relevant for large repos). 
        while comment_url:
            # Make API request to specified url
            async with session.get(comment_url) as response:
                # Because of recursion, check if API request actually gets a correct response
                if response.status == 200:
                    # Convert response to JSON
                    comments = await response.json()
                    # Loop through all comments in JSON response
                    for comment in comments:
                        comment['comment_type'] = comment_type
                        all_comments.append(comment)                        
                    
                    # Check for pagination
                    links = response.headers.get('Link')
                    if links:
                        link_parts = links.split(',')
                        next_link = None
                        for part in link_parts:
                            if 'rel="next"' in part:
                                next_link = part[part.find('<') + 1:part.find('>')]
                                break
                        comment_url = next_link
                    else:
                        comment_url = None
                else:
                    comment_url = None

    # Start aiohttp ClientSession
    async with aiohttp.ClientSession() as session:
        # Get the message associated with PR
        async with session.get(pr_details_url) as pr_response:
            # Check if API request actually gets a correct response
            if pr_response.status == 200:
                # If successful, add PR message to list of all comments.
                pr_details = await pr_response.json()
                pr_details['comment_type'] = 'pull request'
                all_comments.append(pr_details)
 

    
        # Retrieve general review comments
        tasks.append(retrieve_comments(pr_review_comments_url, 'review comment', session))

        # Retrieve issue comments (assuming pull request is treated as an issue)
        tasks.append(retrieve_comments(pr_issue_comments_url, 'issue comment', session))

        # Await all nested comment tasks
        await asyncio.gather(*tasks)  

    return all_comments

# Function based on comment_visual which stores and returns all comments with body as a list.
# Is used in general_semantic_score.py (temporarily).
async def list_of_comments():
    # NOTE: Personal access token with repo permission turned on IS REQUIRED!
    personal_access_token = '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'

    # Headers for the API request
    headers = {'Authorization': f'token {personal_access_token}'}

    # Testing with open pull request at https://github.com/lucidrains/PaLM-rlhf-pytorch/pull/52
    owner = 'IntersectMBO'
    repo = 'plutus'
    pull_number = 5772

    # Test run to retrieve all comments from https://github.com/lucidrains/PaLM-rlhf-pytorch/pull/52
    async with aiohttp.ClientSession(headers=headers,trust_env=True) as session: 
        all_comments = await get_pull_request_comments(owner, repo, pull_number, headers, session)

        comments_with_body = []

        # Collect comments containing a body into a list
        for comment in all_comments:
            if 'body' in comment and comment['body']:
                comments_with_body.append(comment['body'])

        return comments_with_body
