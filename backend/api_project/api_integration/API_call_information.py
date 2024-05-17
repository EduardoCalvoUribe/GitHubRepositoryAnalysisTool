from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from django.conf import settings
from datetime import datetime, timedelta
from collections import Counter
from . import functions
from . import models 
from . import views
import aiohttp
import asyncio
import time
import re
from urllib.parse import urlparse, parse_qs
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import sync_to_async

# This function should return visual on everything and call functions to get all information
@csrf_exempt
async def get_github_information(response):
    start_time = time.time() # Variable to check the runtime of the function
    # owner = 'IntersectMBO'
    # repo = 'govtool'
    
    url = views.process_vue_POST_request(response)
    parsed_variables = views.parse_Github_url_variables(url)
    owner = parsed_variables[1]
    repo = parsed_variables[2]
    print(owner)
    print(repo)
    
    # NOTE: Personal access token with repo permission turned on IS REQUIRED!
    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    # Headers for the API request
    headers = {'Authorization': f'token {personal_access_token}'}

    async with aiohttp.ClientSession(headers=headers) as session:
        results = await handle_pull_requests(session, owner, repo)

        text_to_display = 'It Worked!'

        for page in results:
            for pr in page:
                text_to_display = text_to_display + '<p></b>Information from Pull request:</b> #' + str(pr[0]['number']) + '</p>------------------------------'
                for commit in pr[1]:
                    text_to_display += f"<p><b>Author</b>: {commit['author']['login'] if commit['author'] else 'Unknown'}</p>"
                    text_to_display += f"<p><b>Date</b>: {commit['commit']['author']['date']}</p>"
                    text_to_display += f"<p><b>Message</b>: {commit['commit']['message']}</p>"
                    text_to_display += '<p>----------------------------</p>'
                for comment in pr[2]:
                    text_to_display += f"</b>Type of comment:</b> {comment['comment_type']}</p>"
                    if 'body' in comment and comment['body']:  
                        text_to_display += f"<p></b>Author</b>: {comment['user']['login']}"
                        text_to_display += f"<p></b>Message</b>: {comment['body']}</p>"
                    else:
                        text_to_display += 'No body'
                    text_to_display += '<p>----------------------------</p>'
                text_to_display += '<p></b>------------------------------------------------------------------------</b></p>'

        end_time = time.time() # Variable to check the total runtime of the function
        duration = end_time - start_time # Total runtime of the function
        print(duration) # Printing the duration to compare different functions' speed  

        response = requests.get('https://api.github.com/rate_limit', headers=headers)
        if response.status_code == 200:
            limit_data = response.json()
            remaining_requests = limit_data['rate']['remaining']
            max_requests = limit_data['rate']['limit']
            reset_timestamp = limit_data['rate']['reset']
            reset_time_utc = datetime.utcfromtimestamp(reset_timestamp)
            reset_time_gmt2 = reset_time_utc + timedelta(hours=2)
            
            print(f"Remaining API calls: {remaining_requests}")
            print(f"Maximum API calls: {max_requests}")
            print(f"Reset time (GMT+2): {reset_time_gmt2.strftime('%Y-%m-%d %H:%M:%S')} GMT+2")
        else:
            print("Failed to fetch rate limit information")

        return JsonResponse(text_to_display, safe=False)


async def handle_pull_requests(session, owner, repo):
    pr_url = f'https://api.github.com/repos/{owner}/{repo}/pulls?state=all'
    all_pr_page_urls = await get_all_page_urls(session, pr_url)
    print(all_pr_page_urls)
    process_page_tasks = [asyncio.create_task(process_page(session, url)) for url in all_pr_page_urls]
    page_results = await asyncio.gather(*process_page_tasks) # [ [[pr, [commits], [comments]], [pr, [commits], [comments]]], [[pr, [commits], [comments]], [pr, [commits], [comments]]]] per each page

    return page_results

async def process_page(session, pr_url):
    # Fetch the page of pull requests asynchronously
    async with session.get(pr_url) as response:
        # Convert the response in a JSON response
        pull_requests = await response.json()
        # Initialize a list of tasks to store pull request processing tasks
        tasks = []

        # Iterate over the filtered pull requests to create a task for processing each pull request
        for pull_request in pull_requests:
            # Create a task to process each pull request asynchronously
            process_pr_tasks = asyncio.create_task(process_pull_request(session, pull_request))
            # Append the task to the list of tasks
            tasks.append(process_pr_tasks)

        # Gather the results and wait until all tasks are complete
        pull_results = await asyncio.gather(*tasks)

        # Iterate over the results to save comments to the database
        for pull_result in pull_results:
            pull_request_instance, all_commits, all_comments = pull_result
            for comment in all_comments:
                await sync_to_async(models.Comment.save_comment_to_db)(comment, pull_request_instance)
            for commit in all_commits:
                await sync_to_async(models.Commit.save_commit_to_db)(commit, pull_request_instance)

        return pull_results #[[pr, [commits], [comments]], [pr, [commits], [comments]]] for each pr

async def process_pull_request(session, pull_request):
    # Fetch the commits of a pull request asynchronously
    all_commits = await fetch_commits(session, pull_request)

    # Fetch the comments of a pull request asynchronously
    all_comments = await fetch_comments(session, pull_request)

    pull_request_instance = pull_request
    # Get the PullRequest instance from the database
    # pr_instance = await sync_to_async(models.PullRequest.objects.get_or_create)(
    #     url=pull_request['url'],
    #     defaults={
    #         'name': '',
    #         'updated_at': pull_request['updated_at'],
    #         'date': pull_request['created_at'],
    #         'title': pull_request['title'],
    #         'body': pull_request['body'],
    #         'user': pull_request['user']['login'],
    #         'number': pull_request['number']
    #     }
    # )
    # pull_request_instance = pr_instance[0]

    # Return commits and comments
    return pull_request_instance, all_commits, all_comments #, 

async def fetch_commits(session, pull_request):
    # Construct the URL to fetch the commit information from GitHub
    pull_request_commits_url = pull_request['commits_url'].replace("{/sha}", "")

    # Fetch commits asynchronously
    async with session.get(pull_request_commits_url) as response:
        # Convert the response in a JSON response
        pr_commits = await response.json()

        # Iterate over each commit retrieved
        #for commit in pr_commits:
            # Create Commit object and save it to the database
            #models.Commit.save_commit_to_db(commit)

        # Return the list of commits  
        return pr_commits

async def fetch_comments(session, pull_request):
    pr_comments_reviews_url = pull_request['url'] + '/reviews'
    #pr_comments_reviews_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/reviews'

    # Initialise empty list which will store all comments for a PR
    all_comments = []
    tasks = []

    # Recursive definition which retrieves all comments for a given URL    
    async def retrieve_comments(comment_url, type, session):
        # Make API request to specified url
        #response = requests.get(comment_url, headers=headers)
        async with session.get(comment_url) as response:
            # Because of recursion, check if API request actually gets a correct response
            if response.status == 200:
                # Format response to JSON
                comments = await response.json()
                # Loop through all comments in JSON response
                for comment in comments:
                    comment['comment_type'] = type
                    all_comments.append(comment)
                    #models.Comment.save_comment_to_db(comment, )

                    if type == 'review API':
                        pr_nested_comment_url = pr_comments_reviews_url + f"/{comment['id']}/comments"
                        #pr_nested_comment_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/reviews/{comment['id']}/comments'
                        task = asyncio.create_task(retrieve_comments(pr_nested_comment_url, type, session))
                        tasks.append(task)

    # Retrieve comments from the reviews URL
    # This ensures that all review comments are added to all_comments.
    await retrieve_comments(pr_comments_reviews_url, 'review API', session),
    await asyncio.gather(*tasks)  # Await nested comment tasks

    # Return list containing all comments
    return all_comments





# Can be in another file
async def get_all_page_urls(session, pr_url):
    # Asynchronously fetches the initial page using the provided session and URL, and assigns the response to response
    async with session.get(pr_url) as response:
        # Retrieves the value of the 'Link' header from the response, which contains pagination information
        link_header = response.headers.get('Link')
        print(link_header)
        total_pages = 1 # Default total of pages is 1
        if link_header: 
            # If link header exists, parse it to extract pagination information
            links = parse_link_header(link_header)
            last_page_url = links.get('last')
            if last_page_url:
                # If 'last' page URL exists, extract total number of pages from it
                total_pages = get_page_number_from_url(last_page_url)

    # Construct all page URLs concurrently by appending page numbers to the API call URL
    all_page_urls = [f'{pr_url}&page={page}' for page in range(1, total_pages + 1)]
    return all_page_urls

# Can be in another file
def get_page_number_from_url(url):
    # Parse the URL to extract its components
    parsed_url = urlparse(url)

    # Parse the query string of the URL to extract query parameters
    query_params = parse_qs(parsed_url.query)

    # Extract the value of the 'page' parameter from the query parameters
    # If 'page' parameter does not exist, default to 1
    page_number = query_params.get('page', ['1'])[0]

    # Convert extracted page number to an integer and return it
    return int(page_number)

# Can be in another file
def parse_link_header(link_header):
    # Initialize dictionary to store parsed links
    links = {}
    # Split the link up into individual link sections
    parts = link_header.split(', ')

    # Iterate over each link section
    for part in parts:
        # Split the link section into URL and relation parts
        section = part.split('; ')
        # Extract the URL enclosed within angle brackets
        url = re.findall('<(.+)>', section[0])[0]
        #Extract the URL enclosed within double quotes
        rel = re.findall('"(.+)"', section[1])[0]
        # Add relation type and URL to the links dictionary
        links[rel] = url

    # Return parsed links dictionary
    return links