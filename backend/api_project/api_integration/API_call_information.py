# Copyright 2024 Radboud University, Modern Software Development Techniques

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from . import models, views, general_semantic_score
from .models import Commit, Comment, PullRequest
import aiohttp, asyncio, re
from urllib.parse import urlparse, parse_qs
from asgiref.sync import sync_to_async

@csrf_exempt
async def get_github_information(response):
    """
    Fetches and returns all necessary information from a specific GitHub repository.

    This function is called by the frontend and uses the provided response to extract
    the URL, then fetches all pull requests, commits, and comments for the specified
    GitHub repository. It processes this information and formats it for display.

    Parameters:
    response (HttpRequest): The HTTP request object containing the URL to be processed.

    Returns:
    JsonResponse: A JsonResponse including all information of a specific GitHub repository,
                  formatted as HTML for display purposes.
    """
    # Get repo url from frontend and parse it to get owner and repo name
    repo_url = views.process_vue_POST_request(response)
    parsed_variables = views.parse_Github_url_variables(repo_url)
    owner = parsed_variables[1]
    repo = parsed_variables[2]
    print("Its starting")
    
    # NOTE: Personal access token with repo permission turned on IS REQUIRED!
    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    # Headers for the API request with the correct authentication
    headers = {'Authorization': f'token {personal_access_token}'}

    async with aiohttp.ClientSession(headers=headers) as session:
        # Create a list of all data types to store objects in
        data_list = [[] for i in range(5)]
        # Create repo default to add to database
        defaults = {
                "url": repo_url,
                "name": repo,
                "owner": owner,
                "updated_at": timezone.now()
        }
        # Add repo object to first element of data list
        data_list[0].append(models.Repository(**defaults)) 
        # Add user object to fifth element of data list                      
        data_list[4].append([models.User(login=owner), "repositories", repo_url])

        # Results is a list of each page of a repo, each page has multiple pull requests and each pull request have multiple commits and comments
        results = await handle_fetch_requests(session, owner, repo)

        # Initialize list for tasks to handle a pull request
        pull_request_tasks = []
        # Iterate through all pages including the pull requests
        for page in results:
            for i, pr in enumerate (page):
                # Create task and append to list
                pull_request_tasks.append(asyncio.create_task(pull_request_task(pr, data_list,i)))

        # Wait until all tasks are completed        
        await asyncio.gather(*pull_request_tasks)
        # Add objects to the database in bulk     
        await bulk_create_objects(data_list) 

        # Return JsonResponse to frontend
        response = await sync_to_async(views.homepage_datapackage)(response)
        return response

async def pull_request_task(pr, data_list, i):
    """
    Process a pull request and update the database with the relevant information.

    Parameters:
        pr (list): A list containing the pull request information.
        data_list (list): A list containing the data to be updated in the database.

    Returns:
        None
    """
    # Initalize time variable
    pr_closed_at = timezone.now()
    # Check if pull request is closed or still open
    if pr[0]['state'] == 'closed':
        pr_closed_at = datetime.strptime(pr[0]['closed_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')

    # Create pull request defaults to add to database
    defaults = {
        "url": pr[0]['url'],
        "repo": data_list[0][-1],
        'updated_at': timezone.now(),
        'closed_at': pr_closed_at,
        'date': datetime.strptime(pr[0]['created_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d'),
        'title': pr[0]['title'],
        'body': pr[0]['body'],
        'user': pr[0]['user']['login'],
        'number': pr[0]['number'],
    }

    data_list[1].append(models.PullRequest(**defaults))
    data_list[4].append([models.User(login=pr[0]['user']['login']), "pull_requests", pr[0]['url']])

    # Initialize list for commit handling tasks
    commit_tasks = []
    for commit in pr[1]:
        commit_tasks.append(asyncio.create_task(commit_task(commit, data_list, pr[0]['number'], i)))

    # Initialize list for comment handling tasks
    comment_tasks = []
    for comment in pr[2]:
        comment_tasks.append(asyncio.create_task(comment_task(comment, data_list, i)))

    # Await until all tasks are done
    await asyncio.gather(*commit_tasks)
    await asyncio.gather(*comment_tasks)

async def commit_task(commit, data_list, pr_num,i):
    """
    Process a commit and add it to the data list.

    Parameters:
        commit (dict): The commit information.
        data_list (list): The list containing data.

    Returns:
        list: The updated data list.
    """
    # Calculate the semantic score of commits
    commit_semantic_score = await general_semantic_score.calculateWeightedCommitSemanticScore(commit, 0.33, 0.33, 0.34, commit['commit']['url'],pr_num)
    # Initialize user_login variable to check for none types
    user_login = ""
    # If commit author is not none, add author name to variable
    if commit['author'] != None:
        user_login = commit['author']['login']
    
    # Create commit defaults to add to database
    defaults = {
        "url": commit['commit']['url'],
        "pull_request": data_list[1][i],
        "name": commit['commit']['message'],
        "title": commit['commit']['message'],
        "user": user_login,#commit['author']['login'],
        "date": datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d'),
        "semantic_score": commit_semantic_score,
        "updated_at": timezone.now(),
    }

    data_list[2].append(models.Commit(**defaults))            
    data_list[4].append([models.User(login=user_login), "commits", commit['commit']['url']]) 

    return data_list

async def comment_task(comment, data_list,i):
    """
    Process a comment and add it to the data list.

    Parameters:
        comment (dict): The comment to be processed.
        data_list (list): The list containing the data.

    Returns:
        list: The updated data list.
    """
    # Calculate comment semantic score
    comment_semantic_score = general_semantic_score.calculateWeightedCommentSemanticScore(comment['body'], 0.5, 0.5)
    # Initialize variables to be used in defaults later
    commit_id = ''
    comment_date = None
    comment_url = None
    # Check comment type because of different endpoint attributes
    if comment['comment_type'] == 'review comment':
        commit_id = comment['commit_id']
        comment_date = comment['created_at'] # this could be submitted_at
        comment_url = comment['html_url']
    else:
        comment_date = comment['created_at']
        comment_url = comment['url']

    # Create comment defaults to add comment to database
    defaults = {
        "url" : comment_url,
        "pull_request": data_list[1][i],
        "date": datetime.strptime(comment_date, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d'),
        "updated_at": timezone.now(),
        "body": comment['body'],
        "user": comment['user']['login'],
        "semantic_score": comment_semantic_score,
        "comment_type": comment['comment_type'],
        "commit_id": commit_id
    }
    
    data_list[3].append(models.Comment(**defaults)) # Append comment to list of comments
    data_list[4].append([models.User(login=comment['user']['login']), "comments", comment_url])

    return data_list

async def bulk_create_objects(data_list):
    """
    Bulk creates objects in the database.

    This function takes a list of objects and bulk creates them in the database.

    Parameters:
    data_list (list): A list of objects to be bulk created in the database.

    Returns:
    None
    """
    repo = data_list[0][0]
    repo_db, created = await sync_to_async(models.Repository.objects.update_or_create)(url=repo.url, defaults={'name': repo.name, 'owner': repo.owner, 'updated_at': repo.updated_at})
    tasks = []
    tasks.append(asyncio.create_task(sync_to_async(create_pull_requests)(data_list, repo_db)))
    tasks.append(asyncio.create_task(sync_to_async(create_comments)(data_list, repo_db)))
    tasks.append(asyncio.create_task(sync_to_async(create_commits)(data_list, repo_db)))
    tasks.append(asyncio.create_task(create_and_update_user_data(data_list[4], repo_db)))
    await asyncio.gather(*tasks)

def create_pull_requests(data_list, repo_db):
    """
    Create or update pull requests in the database.

    Parameters:
        data_list (list): A list containing pull request data.
        repo_db (str): The name of the repository in the database.

    Returns:
        None
    """
    pull_set = set()
    for pull in data_list[1]:
        models.PullRequest.objects.update_or_create(url=pull.url, defaults={'repo': repo_db, 'updated_at': pull.updated_at, 'closed_at': pull.closed_at, 'date': pull.date, 'title': pull.title, 'body': pull.body, 'user': pull.user, 'number': pull.number})
        pull_set.add(pull.url)
    update_model_data(repo_db, "pull_requests_list", list(pull_set)) # add pull request to list of pull requests in repo

def create_comments(data_list, repo_db):
    """
    Create comments in the database based on the provided data list.

    Parameters:
        data_list (list): A list containing the data for commits and comments.
        repo_db: The database object.

    Returns:
        None
    """
    commit_set = set()
    for commit in data_list[2]:
        models.Commit.objects.update_or_create(url=commit.url, defaults={'pull_request': PullRequest.objects.get(url=commit.pull_request.url), 'name': commit.name, 'title': commit.title, 'user': commit.user, 'date': commit.date, 'semantic_score': commit.semantic_score, 'updated_at': commit.updated_at})
        commit_set.add(commit.url)
    update_model_data(repo_db, "commits_list", list(commit_set)) # add commit to list of commits in repo

def create_commits(data_list, repo_db):
    """
    Create commits in the database based on the provided data list.

    Parameters:
        data_list (list): A list containing the data for commits and comments.
        repo_db: The database object.

    Returns:
        None
    """
    comment_set = set()
    for comment in data_list[3]:
        # Handle empty comment
        body = comment.body if comment.body is not None else ''
        models.Comment.objects.update_or_create(url=comment.url, defaults={'pull_request': PullRequest.objects.get(url=comment.pull_request.url), 'date': comment.date, 'updated_at': comment.updated_at, 'body': body, 'user': comment.user, 'semantic_score': comment.semantic_score, 'comment_type': comment.comment_type, 'commit_id': comment.commit_id})
        comment_set.add(comment.url)
    update_model_data(repo_db, "comments_list", list(comment_set)) # add comment to list of comments in repo


async def create_and_update_user_data(all_users, repo_db):
    """
    Creates or updates user data in the database.

    Parameters:
        all_users (list): A list of user data.
        repo_db: The repository database.

    Returns:
        None
    """
    users_set = set()
    comment_set = set()
    commit_set = set()
    for user in all_users:
        user_db, created = await sync_to_async(models.User.objects.update_or_create)(login=user[0].login)
        if(user[1] == "comments"):
            comment_set.add(user[2])
        else:
            commit_set.add(user[2])
        users_set.add(user[0].login)
    await sync_to_async(update_model_data)(user_db, "comments", list(comment_set)) # add comment to list of comments in repo
    await sync_to_async(update_model_data)(user_db, "commits", list(commit_set)) # add commit to list of commits in repo
    await sync_to_async(update_model_data)(repo_db, "users_list", list(users_set)) # add user to list of users in repo

from django.db.models import F

def update_model_data(model, related_data_field, related_data_url):
    """
    Update the model data by appending a related data URL to a specified field.

    Parameters:
        model: The model object to update.
        related_data_field: The name of the field in the model to update.
        related_data_url: The URL of the related data to append.

    Returns:
        None
    """
    current = getattr(model, related_data_field)
    current.extend(related_data_url)
    setattr(model, related_data_field, current)  # Use set union for unique values
    model.save()

async def handle_fetch_requests(session, owner, repo):
    """
    Fetches all pages of pull requests for a GitHub repository and processes them.

    This function constructs the URL to fetch pull requests for the specified repository,
    retrieves all pages of pull requests, and processes each page concurrently.

    Parameters:
    session (aiohttp.ClientSession): The asynchronous session with the authentication headers included.
    owner (str): The owner of the GitHub repository.
    repo (str): The name of the GitHub repository.

    Returns:
    list: A list containing the processed results of all pages, where each page contains
          lists of pull requests, each with their commits and comments.
    """
    # API link to fetch all pull requests
    pr_url = f'https://api.github.com/repos/{owner}/{repo}/pulls?state=all'
    # Calls function to get the API links for pulls for all pages (max of 35 pull requests per page)
    all_pr_page_urls = await get_all_page_urls(session, pr_url)
    # Create all a task to process each page concurrently
    process_page_tasks = [asyncio.create_task(process_page(session, url)) for url in all_pr_page_urls]
    page_results = await asyncio.gather(*process_page_tasks) # [ [[pr, [commits], [comments]], [pr, [commits], [comments]]], [[pr, [commits], [comments]], [pr, [commits], [comments]]]] per each page

    # Return results of all pages
    return page_results

async def process_page(session, pr_url):
    """
    Processes a single page of pull requests for a GitHub repository.

    This function fetches all pull requests on the specified page, processes each
    pull request to fetch its commits and comments, and returns the results.

    Parameters:
    session (aiohttp.ClientSession): The asynchronous session with the authentication headers included.
    pr_url (str): The URL to fetch all pull requests on a page.

    Returns:
    list: A list of pull requests, where each pull request contains its commits and comments.
    """
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
        return pull_results #[[[pr, [commits], [comments]], [pr, [commits], [comments]]] for each pr

async def process_pull_request(session, pull_request):
    """
    Processes a singular pull request by fetching all comments and commits on that pull request

    Parameters:
    session (aiohttp.ClientSession): The asynchronous session with the authentication headers included.
    pull_request (dict): A JSON response representing a pull request.

    Returns:
    tuple: A tuple containing a list of commits and a list of comments for the pull request.
    """

    owner = pull_request['base']['repo']['owner']['login']
    repo = pull_request['base']['repo']['name']
    pull_number = pull_request['number']
    commits_task = asyncio.create_task(fetch_commits(session, pull_request))
    comments_task = asyncio.create_task(fetch_comments(session, pull_request))
    
    all_commits = await commits_task
    all_comments = await comments_task

    # Return commits and comments
    return pull_request, all_commits, all_comments 

async def fetch_commits(session, pull_request):
    """
    Function that retrieves all commits of a pull request

    Parameters:
    session (aiohttp.ClientSession): The asynchronous session with the authentication headers included.
    pull_request (dict): A JSON response representing a pull request.

    Returns:
    list: A list of commits for the pull request.
    """
    # Construct the URL to fetch the commit information from GitHub
    pull_request_commits_url = pull_request['commits_url'].replace("{/sha}", "")

    # Get all pagination urls to be able to get all commits
    all_commit_urls = await get_all_page_urls(session, pull_request_commits_url)

    # Create tasks to process each page concurrently
    tasks = [asyncio.create_task(fetch_commit_page(session, url)) for url in all_commit_urls]
    
    # Wait until all tasks are complete
    commit_pages = await asyncio.gather(*tasks)

    # Flatten the results list to get a list with all commits
    pr_commits = [commit for page in commit_pages for commit in page]

    # Return the list of commits
    return pr_commits
    
async def fetch_commit_page(session, url):
    """
    Fetches a single page of commits asynchronously.

    Parameters:
    session (aiohttp.ClientSession): The asynchronous session with the authentication headers included.
    url (str): The URL to fetch commits from.

    Returns:
    list: A list of commits for the given page.
    """
    async with session.get(url) as response:
        # Convert the response to a JSON object
        commits = await response.json()

        # Return the commits on one page
        return commits

async def fetch_comments(session, pull_request):
    """
    Function that retrieves all comments of a pull request

    Parameters:
    session: the asynchronous session with the authentication headers included
    pull_request: a json response of a pull request

    Returns:
    List of all comments of a pull request
    """
    # Initialise empty list which will store all comments for a PR
    all_comments = []
    tasks = []

    # Recursive definition which retrieves all comments for a given URL    
    async def retrieve_comments(comment_url, comment_type, session):
        """
        Recursively retrieves nested comments within a pull request.

        Parameters:
        comment_url (str): The URL to fetch comments from.
        type (str): The type of the comment (review, comment, or issue).
        session (aiohttp.ClientSession): The asynchronous session with the authentication headers included.
        """
        await asyncio.sleep(0.1)
        # Get all pagination urls to be able to get all comments
        comment_page_urls = await get_all_page_urls(session, comment_url)
        # Create tasks to process each comment page concurrently
        comment_tasks = [asyncio.create_task(fetch_comment_page(session, url)) for url in comment_page_urls]
        # Wait until all tasks are complete
        comment_pages = await asyncio.gather(*comment_tasks)

        # Check if comment is a pull request comment. This is handled differently
        if comment_type == "pull request":
            for comment in comment_pages:    
                comment['comment_type'] = str(comment_type)
                all_comments.append(comment)
        else:
            # Iterate over each response and add comments to the list
            for page in comment_pages:
                for comment in page:
                    comment['comment_type'] = str(comment_type)
                    all_comments.append(comment)

    # API endpoint for PR message
    pr_details_url = pull_request['url']
    pr_task = asyncio.create_task(fetch_comment_page(session, pr_details_url))
    tasks.append(pr_task)

    # API endpoint for review comments
    pr_review_comments_url = pr_details_url + '/comments'
    review_task = asyncio.create_task(retrieve_comments(pr_review_comments_url, 'review comment', session))
    tasks.append(review_task)

    # API endpoint for issue comments
    pr_issue_comments_url = pr_details_url.replace("pulls", "issues") + "/comments"
    issue_task = asyncio.create_task(retrieve_comments(pr_issue_comments_url, 'issue comment', session))
    tasks.append(issue_task)

    # Wait until all tasks are completed
    await asyncio.gather(*tasks)

    # Return list containing all comments
    return all_comments

async def fetch_comment_page(session, url):
    """
    Fetches a page of comments for a given URL.

    Parameters:
    session (aiohttp.ClientSession): The asynchronous session with the authentication headers included.
    url (str): The URL to fetch comments from.

    Returns:
    dict: JSON response containing comments.
    """
    # Make a GET request to the provided URL to fetch comments
    async with session.get(url) as response:
            # Ensure that the response is succesful
            response.raise_for_status()
            # Create json object from response
            comments = await response.json()
            # Return all comments on a single page
            return comments


async def get_all_page_urls(session, pr_url):
    """
    Retrieves all URLs for every page of pull requests from the initial URL.

    This function asynchronously fetches the initial page of pull requests using
    the provided session and URL, checks for pagination information in the 
    'Link' header, and constructs a list of URLs for all pages.

    Parameters:
    session (aiohttp.ClientSession): The asynchronous session with the 
                                     authentication headers included.
    pr_url (str): The initial URL for the pull requests.

    Returns:
    list: A list containing URLs for all pages of pull requests.
    """
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

    # Determine if the pr_url already contains a query parameter
    separator = '&' if '?' in pr_url else '?'

    # Construct all page URLs concurrently by appending page numbers to the API call URL
    all_page_urls = [f'{pr_url}{separator}page={page}' for page in range(1, total_pages + 1)]
    return all_page_urls

def get_page_number_from_url(url):
    """
    Extracts the page number from a given URL.

    This function parses the query string of the URL to find the 'page' parameter
    and returns its value as an integer. If the 'page' parameter does not exist,
    it defaults to 1.

    Parameters:
    url (str): The URL from which the page number needs to be extracted.

    Returns:
    int: The page number extracted from the URL.
    """
    # Parse the URL to extract its components
    parsed_url = urlparse(url)

    # Parse the query string of the URL to extract query parameters
    query_params = parse_qs(parsed_url.query)

    # Extract the value of the 'page' parameter from the query parameters
    # If 'page' parameter does not exist, default to 1
    page_number = query_params.get('page', ['1'])[0]

    # Convert extracted page number to an integer and return it
    return int(page_number)

def parse_link_header(link_header):
    """
    Parses the 'Link' header from an HTTP response to extract pagination URLs.

    The 'Link' header typically contains multiple URLs, each with a relation type
    such as 'next', 'prev', 'first', and 'last', indicating their purpose in the
    pagination of API responses. This function splits the header into its 
    constituent parts and extracts these URLs into a dictionary for easy access.

    Parameters:
    link_header (str): The 'Link' header string from an HTTP response, which 
                       contains URLs and their relation types.

    Returns:
    dict: A dictionary where the keys are relation types (e.g., 'next', 'prev', 
          'first', 'last') and the values are the corresponding URLs as strings. 
    """
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

def calculate_semantic_score_user(user):
    """
    Calculate the average semantic score for a given repository.

    Args:
        user: A user object

    Returns:
        float: The average semantic score of the user. If there are no comments or commits,
               the function returns 0 to avoid division by zero.
    """
    total_semantic = 0
    user_comments_urls = user.comments  # user.comments is a list of comment URLs
    user_commits_urls = user.commits  # user.commits is a list of commit URLs

    # Fetch all comments based on URLs
    comments = Comment.objects.filter(url__in=user_comments_urls)
    commits = Commit.objects.filter(url__in=user_commits_urls)
    
    # Sum the semantic scores from comments
    for comment in comments:
        total_semantic += comment.semantic_score

    # Sum the semantic scores from commits
    for commit in commits:
        total_semantic += commit.semantic_score
    
    total_urls = len(user_comments_urls) + len(user_commits_urls)
    
    return total_semantic / total_urls if total_urls > 0 else 0  # Prevent division by zero

def calculate_semantic_score_repo(repo):
    """
    Calculate the average semantic score for a given repository.

    Parameters:
        repo: A repository object

    Returns:
        float: The average semantic score of the repository. If there are no comments or commits,
               the function returns 0 to avoid division by zero.
    """
    total_semantic = 0
    user_comments_urls = repo.comments_list  # user.comments is a list of comment URLs
    user_commits_urls = repo.commits_list  # user.commits is a list of commit URLs

    # Fetch all comments based on URLs
    comments = Comment.objects.filter(url__in=user_comments_urls)
    commits = Commit.objects.filter(url__in=user_commits_urls)
    
    # Sum the semantic scores from comments
    for comment in comments:
        total_semantic += comment.semantic_score

    # Sum the semantic scores from commits
    for commit in commits:
        total_semantic += commit.semantic_score
    
    total_urls = len(user_comments_urls) + len(user_commits_urls)
    
    return total_semantic / total_urls if total_urls > 0 else 0  # Prevent division by zero