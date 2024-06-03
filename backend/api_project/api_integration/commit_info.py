from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from django.conf import settings
from datetime import datetime
from collections import Counter
from . import functions
from .models import Commit 
import aiohttp
import asyncio
import time
import re
from urllib.parse import urlparse, parse_qs
import json

# Helper function which uses repo_total_commits function to retrieve number of commits
async def get_commit_count(request):
    owner = 'lucidrains'
    repo = 'PaLM-rlhf-pytorch'
    pull_number = 52
    start_date = "2020-01-01"
    end_date = "2024-06-01"
    status = "all"
    set = "all"
    commit_count = await repo_total_commits(request, owner, repo, pull_number, start_date, end_date, status, set)
    return commit_count

# Function which creates a package containing the commit count
async def commit_count_JSON(request):
    
    commit_count = await get_commit_count(request)
    
    # Create JSON package containing the comment count
    try:
        # Add commit count to JSON data
        data = {
            "commit_count": commit_count
        } 
        # 
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception as e:
        error_data = {"error": str(e)}
        return HttpResponse(json.dumps(error_data), content_type='application/json', status=500)

async def printCommitCountJSON(request):
    owner = 'lucidrains'
    repo = 'PaLM-rlhf-pytorch'
    pull_number = 52
    
    commit_JSON_response = await commit_count_JSON(request)
    # Deserialize JSON from the HttpResponse
    commit_JSON = json.loads(commit_JSON_response.content)
    # Return commit_JSON as JsonResponse. 
    return JsonResponse(commit_JSON)


async def repo_total_commits(request, owner, repo, pull_number, start_date, end_date, status, set):
    # TODO: What should the final reponse be to be able to be used by frontend
    # start/end_date = YYYY-MM-DD
    # status = open, closed or all (pull requests)
    # set = general, pull or all

    # Specify time frame in year month day format
    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").isoformat()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").isoformat()

    # Creating variables to be seen outside of coming if statement
    text_to_display = ''
    total_commit_amount = 0
    user_commit_count = {}

    # Check if only commits of a specific pull request are needed
    if pull_number == None: # All commits should be requested
        # Check if only commits of a certain pull are required the commits in general
        if set != 'pull':
            # Call function to get the commits that do not belong to a pull request
            repo_text_to_display, repo_total_commit_amount, repo_user_commit_count = general_repo_commits(request, owner, repo, start_date, end_date)
            # Add data to created variables
            user_commit_count = repo_user_commit_count # List of users with there respective commit count
            total_commit_amount = repo_total_commit_amount # Total amount of commits not belonging to a pull request
            text_to_display = repo_text_to_display # Text to display on the webpage (might not be necessary in final product)

        # Checks if the commits of the pull requests are required by the api call
        if set != 'general':
            # Call function to get the commits that do belong to a pull request
            pull_text_to_display, pull_total_commit_amount, pull_user_commit_count = await pull_commits_async(request, owner, repo, start_date, end_date, status)
            # Add data to the created variables
            total_commit_amount += pull_total_commit_amount
            text_to_display += pull_text_to_display
            user_commit_count = Counter(user_commit_count) + Counter(pull_user_commit_count)

    else: # Only commits of a specific pull request are needed
        text_to_display, total_commit_amount, user_commit_count = specific_pull_commits(request, owner, repo, pull_number)

    # Making Httpresponse text
    text_to_display_neat = ''

    # If/else statement to properly format the date if a start and end date were given (might not be necessary in the final product)
    if start_date:
        text_to_display_neat = f"Total Commits: {total_commit_amount} from {start_date.split('T')[0]} to {end_date.split('T')[0]}</p>"
    else:
        text_to_display_neat = f"Total Commits: {total_commit_amount}"
    text_to_display_neat += "<p>Commits by each user:</p>"
    for user, count in user_commit_count.items():
        text_to_display_neat += f"<p>{user}: {count}</p>"

    text_to_display_neat = text_to_display_neat + text_to_display

    # Return text_to_display in Django HttpResponse format (in order to display on URL)
    # return HttpResponse(text_to_display_neat)

    # Alternative return statement for testing purposes. Returns total_commit_amount for commit count JSON package function.
    return total_commit_amount

def general_repo_commits(request, owner, repo, start_date, end_date):
    # API call for the commits not associated to a PR
    repo_commits_url = f'https://api.github.com/repos/{owner}/{repo}/commits?since={start_date}&until={end_date}'

    # Creation of variables to be returned
    text_to_display = ""
    total_commit_amount = 0
    user_commit_count = {}

    # As long as there are other pages the loop should keep running
    while repo_commits_url:
        repo_commits_response = functions.get_api_reponse(repo_commits_url)
        repo_commits = repo_commits_response.json()

        for commit in repo_commits:
        # TODO: Add variable for branch the commit was committed to
            # Increment total commit count
            total_commit_amount += 1
            # Get the author's login
            commit_author = commit['author']['login'] if commit['author'] else 'Unknown'
            # Increase the commit count of a user
            user_commit_count[commit_author] = user_commit_count.get(commit_author, 0) + 1

            # Extracting relevant information
            commit_date = commit['commit']['author']['date']
            commit_message = commit['commit']['message']

            # Dividing the different commits with a visible line
            text_to_display += "-------------------</p>"

            # Constructing commit information in the display text
            text_to_display += "<p><b>Author</b>: " + commit_author + "</p>"
            text_to_display += "<p><b>Date</b>: " + commit_date + "</p>"
            text_to_display += "<p><b>Message</b>: " + commit_message + "</p>"

        # Check if there are more commits on a different page
        if 'next' in repo_commits_response.links:
            repo_commits_url = repo_commits_response.links['next']['url']
        else:
            # If there are no other pages, the url should be given the None value to stop the loop from running
            repo_commits_url = None

    return text_to_display, total_commit_amount, user_commit_count
    
def specific_pull_commits(request, owner, repo, pull_number):
    text_to_display = ""
    total_commit_amount = 0
    user_commit_count = {}

    pr_commits_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/commits'

    # As long as there are other pages the loop should keep running
    while pr_commits_url:
        pr_response = functions.get_api_reponse(pr_commits_url)
        pr_commits = pr_response.json()

        # Iterate over commits associated with the pull request
        for commit in pr_commits:
            total_commit_amount += 1
            # Get the author's login
            commit_author = commit['author']['login'] if commit['author'] else 'Unknown'
            # Increase the commit count of a user
            user_commit_count[commit_author] = user_commit_count.get(commit_author, 0) + 1

            # Extracting relevant information
            commit_date = commit['commit']['author']['date']
            commit_message = commit['commit']['message']

            text_to_display += "-------------------</p>"
            # Constructing commit information
            text_to_display += "<p><b>Author</b>: " + commit_author + "</p>"
            text_to_display += "<p><b>Date</b>: " + commit_date + "</p>"
            text_to_display += "<p><b>Message</b>: " + commit_message + "</p>"
        
        if ('next' in pr_response.links):
            pr_commits_url = pr_response.links['next']['url']
        else:
            pr_commits_url = None

    return text_to_display, total_commit_amount, user_commit_count

async def pull_commits_async(request, owner, repo, start_date, end_date, status):
    start_time = time.time() # Variable to check the runtime of the function

    # Creating variables to be return by this function
    text_to_display = ""
    total_commit_amount = 0
    user_commit_count = {}

    # Creating headers for correct authorization access
    headers = {'Authorization': f'token {settings.GITHUB_PERSONAL_ACCESS_TOKEN}'}

    # Starting an asynchronized session to be able to run multiple processes at once
    # Headers should be given to session for authentication purposes
    async with aiohttp.ClientSession(headers=headers) as session: 
        # API call link to get all pulls
        pr_url = f'https://api.github.com/repos/{owner}/{repo}/pulls?state={status}' 
        # Starting a function to get all pages API links of pull requests of a certain repository
        all_page_urls = await get_all_page_urls(session, pr_url) 
        # Creating tasks to to process all pages asynchronously (at the same time)
        all_pages_tasks = [asyncio.create_task(process_page(session, url, start_date, end_date)) for url in all_page_urls] 

        # Wait until all created tasks are complete and put into the results
        results = await asyncio.gather(*all_pages_tasks)

        # Looping through the results of the processing pages task
        for result1 in results:
            # At the moment, the nested loop is still needed because of some weird returns in other functions. TODO: to be fixed
            for result2 in result1: 
                sub_text_to_display, sub_total_commit_amount, sub_user_commit_count = result2
                # Updating the already created variables with the new result information
                text_to_display += sub_text_to_display
                total_commit_amount += sub_total_commit_amount
                user_commit_count = Counter(user_commit_count) + Counter(sub_user_commit_count)

    end_time = time.time() # Variable to check the total runtime of the function
    duration = end_time - start_time # Total runtime of the function
    print(duration) # Printing the duration to compare different functions' speed  
    return text_to_display, total_commit_amount, user_commit_count

async def get_all_page_urls(session, pr_url):
    # Asynchronously fetches the initial page using the provided session and URL, and assigns the response to response
    async with session.get(pr_url) as response:
        # Retrieves the value of the 'Link' header from the response, which contains pagination information
        link_header = response.headers.get('Link')
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

async def process_page(session, pr_url, start_date, end_date):
    # Fetch the page of pull requests asynchronously
    async with session.get(pr_url) as response:
        # Convert the response in a JSON response
        pull_requests = await response.json()
        # Filter the pull requests based on the date of the last update
        filtered_pull_requests = [pr for pr in pull_requests if start_date <= pr['updated_at'] <= end_date]
        # Initialize a list of tasks to store pull request processing tasks
        tasks = []

        # Iterate over the filtered pull requests to create a task for processing each pull request
        for pull_request in filtered_pull_requests:
            # Create a task to process each pull request asynchronously
            task = asyncio.create_task(process_pull_request(session, pull_request, start_date, end_date))
            # Append the task to the list of tasks
            tasks.append(task)

        # Gather the results and wait until all tasks are complete
        results = await asyncio.gather(*tasks)

        return results
    
async def process_pull_request(session, pull_request, start_date, end_date):
    # Fetch the commits of a pull request asynchronously
    commits = await fetch_commits_for_pull_requests(session, pull_request, start_date, end_date)
    text_to_display = "" # HTML text to display the commit information
    total_commit_amount = 0 # Total number of commits
    user_commit_count = {} # Dictionary to store commit counts per user

    # Iterate over each commit
    for commit in commits:
        total_commit_amount += 1 # Increment commit total
        commit_author = commit['author'] # Determine commit author
        user_commit_count[commit_author] = user_commit_count.get(commit_author, 0) + 1 # Update dictionary

        # Construct HTML representation of commit information
        text_to_display += "-------------------</p>"
        text_to_display += f"<p><b>Author</b>: {commit['author']}</p>"
        text_to_display += f"<p><b>Date</b>: {commit['date']}</p>"
        text_to_display += f"<p><b>Pull Request</b>: Pull Request #{commit['pull_request_number']}: {commit['pull_request_title']}</p>"
        text_to_display += f"<p><b>Message</b>: {commit['message']}</p>"

    # Return processed data
    return text_to_display, total_commit_amount, user_commit_count

async def fetch_commits_for_pull_requests(session, pull_request, start_date, end_date):
    # Construct the URL to fetch the commit information from GitHub
    pull_request_commits_url = pull_request['commits_url'].replace("{/sha}", "")

    # Fetch commits asynchronously
    async with session.get(pull_request_commits_url) as response:
        # Convert the response in a JSON response
        pr_commits = await response.json()
        # Initialize an empty list to store filtered commits
        commits = []

        # Iterate over each commit retrieved
        for commit in pr_commits:
            # Extract the date of the commit and format it in iso format
            commit_date = datetime.strptime(commit['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ").isoformat()

            # Check if the commit data falls between the specified start and end date range
            if start_date <= commit_date <= end_date:
                # Extract commit author
                commit_author = commit['author']['login'] if commit['author'] else 'Unknown'
                # Extract commit date
                commit_date = commit['commit']['author']['date']
                # Extract commit message
                commit_message = commit['commit']['message']
                # Append filtered commit details to the list of commits
                commits.append({
                    'author': commit_author,
                    'date': commit_date,
                    'message': commit_message,
                    'pull_request_number': pull_request['number'],
                    'pull_request_title': pull_request['title']
                })

                # Create Commit object and save it to the database
                Commit.save_commit_to_db(commit)

        # Return the list of commits  
        return commits

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