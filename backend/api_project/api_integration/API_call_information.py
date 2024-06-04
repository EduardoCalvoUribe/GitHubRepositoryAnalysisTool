from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from collections import Counter
from . import functions, models, views, general_semantic_score
from .models import Commit, Comment, User, Repository, PullRequest
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
    start_time = time.time() # Variable to check the runtime of the function
    #owner = 'lucidrains'
    #repo = 'PaLM-rlhf-pytorch'
    
    repo_url = views.process_vue_POST_request(response)
    parsed_variables = views.parse_Github_url_variables(repo_url)
    print(parsed_variables)
    owner = parsed_variables[1]
    repo = parsed_variables[2]
    
    # NOTE: Personal access token with repo permission turned on IS REQUIRED!
    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    # Headers for the API request
    headers = {'Authorization': f'token {personal_access_token}'}

    async with aiohttp.ClientSession(headers=headers) as session:
        repo_db = models.Repository(name = repo,
                               owner = owner,
                               url = repo_url,
                               updated_at = timezone.now(),
                               token = '')#settings.GITHUB_PERSONAL_ACCESS_TOKEN)
        await sync_to_async(repo_db.save)()

        
        user, created = await sync_to_async(models.User.objects.update_or_create)(login=owner)
        # list = user.repositories
        # print(type(list), "repo")
        # #list.update({repo_db.name:repo_db.url})
        # list.append(repo_db.url)
        # user.repositories = list 
        # await sync_to_async(user.save)()
        await update_model_data(user, "repositories", repo_db.url)
        #await sync_to_async(user.save)()


        # Results is a list of each page of a repo, each page has multiple pull requests and each pull request have multiple commits and comments
        results = await handle_fetch_requests(session, owner, repo)

        # Text to display that everything went correctly
        text_to_display = 'It Worked!'

        # Code used to check how many API calls are used, how many you have left and when it resets
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

        # This for loop is only for creating displayable text on a website (not important for loop and can be deleted in end)
        for page in results:
            pulls = []
            for pr in page:
                # Combine URL and repo checks for update_or_create
                defaults = {
                    'updated_at': timezone.now(),
                    'date': datetime.strptime(pr[0]['created_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d'),
                    'title': pr[0]['title'],
                    'body': pr[0]['body'],
                    'user': pr[0]['user']['login'],
                    'number': pr[0]['number'],
                }

                pull_db, created = await sync_to_async(models.PullRequest.objects.update_or_create)(
                    url=pr[0]['url'], repo=repo_db, defaults=defaults
                )
                await sync_to_async(pull_db.save)()

                user, created = await sync_to_async(models.User.objects.update_or_create)(login=pull_db.user)
                # list = user.pull_requests
                # list.append(pull_db.url)
                # user.pull_requests = list
                await update_model_data(user, "pull_requests", pull_db.url)
                await update_model_data(repo_db, "pull_requests_list", pull_db.url)
                #await sync_to_async(user.save)()


                text_to_display = text_to_display + '<p></b>Information from Pull request:</b> #' + str(pr[0]['number']) + '</p>------------------------------'
                for commit in pr[1]:
                    commit_semantic_score = general_semantic_score.calculate_weighted_commit_semantic_score(commit, 0.33, 0.33, 0.34, commit['commit']['url'])

                    defaults = {
                        "name": commit['commit']['message'],
                        "title": commit['commit']['message'],
                        "user": commit['author']['login'],
                        "date": datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d'),
                        "semantic_score": commit_semantic_score,
                        "updated_at": timezone.now(),
                    }
                    # commit_db = models.Commit(pull_request = pull_db,
                    #                         name = commit['commit']['message'],
                    #                         url = commit['commit']['url'],
                    #                         title = commit['commit']['message'],
                    #                         user = commit['author']['login'],
                    #                         date = datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d'),
                    #                         semantic_score = commit_semantic_score,
                    #                         updated_at = timezone.now())
                    
                    commit_db,created = await sync_to_async(models.Commit.objects.update_or_create)(url = commit['commit']['url'], pull_request = pull_db, defaults= defaults )
                    await sync_to_async(commit_db.save)()

                    user, created = await sync_to_async(models.User.objects.update_or_create)(login=commit_db.user)
                    await update_model_data(user, "commits", commit_db.url)
                    # list = user.commits
                    # list.append(commit_db.url)
                    # user.commits = list
                    #await sync_to_async(user.save)()


                    text_to_display += f"<p><b>Author</b>: {commit['author']['login'] if commit['author'] else 'Unknown'}</p>"
                    text_to_display += f"<p><b>Date</b>: {commit['commit']['author']['date']}</p>"
                    text_to_display += f"<p><b>Message</b>: {commit['commit']['message']}</p>"
                    text_to_display += '<p>----------------------------</p>'
                for comment in pr[2]:
                    comment_semantic_score = general_semantic_score.calculate_weighted_comment_semantic_score(comment['body'], 0.5, 0.5)
                    commit_id = ''
                    if comment['comment_type'] is 'review comment':
                        commit_id = comment['commit_id']
                    defaults = {
                        "date": datetime.strptime(comment['created_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d'),
                        "updated_at": timezone.now(),
                        "body": comment['body'],
                        "user": comment['user']['login'],
                        "semantic_score": comment_semantic_score,
                        "comment_type": comment['comment_type'],
                        "commit_id": commit_id
                    }
                    # comment_db = models.Comment(pull_request = pull_db,
                    #                             url = comment['url'],
                    #                             date = datetime.strptime(comment['created_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d'),
                    #                             updated_at = timezone.now(),
                    #                             body = comment['body'],
                    #                             user = comment['user']['login'],
                    #                             semantic_score = comment_semantic_score)
                    comment_db, created = await sync_to_async(models.Comment.objects.update_or_create)(url = comment['url'],pull_request = pull_db, defaults=defaults)
                    await sync_to_async(comment_db.save)()

                    user, created = await sync_to_async(models.User.objects.update_or_create)(login=comment_db.user)
                    await update_model_data(user, "comments", comment_db.url)
                    # list = user.comments
                    # list.append(comment_db.url)
                    # user.comments = list
                    #await sync_to_async(user.save)()



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

        # Return JsonResponse to frontend (return can eventually be deleted/reformed)
        return JsonResponse(text_to_display, safe=False)


async def update_model_data(model, related_data_field, related_data_url):
    print(related_data_field)
    current = getattr(model, related_data_field)
    current.append(related_data_url)
    print(current)
    setattr(model, related_data_field, current)  # Use set union for unique values
    await sync_to_async(model.save)()
    #return model



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
    TODO: Might want to add creation of pull request instance for database

    Parameters:
    session (aiohttp.ClientSession): The asynchronous session with the authentication headers included.
    pull_request (dict): A JSON response representing a pull request.

    Returns:
    tuple: A tuple containing a list of commits and a list of comments for the pull request.
    """
    # Fetch the commits of a pull request asynchronously
    all_commits = await fetch_commits(session, pull_request)

    # Fetch the comments of a pull request asynchronously
    all_comments = await fetch_comments(session, pull_request)

    # Return commits and comments
    return pull_request, all_commits, all_comments 

async def fetch_commits(session, pull_request):
    """
    Function that retrieves all commits of a pull request
    # TODO: Unsure if pages are also a thing here that need to be taken into account

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
    # TODO: Unsure if pages are also a thing here that need to be taken into account

    Parameters:
    session: the asynchronous session with the authentication headers included
    pull_request: a json response of a pull request

    Returns:
    List of all comments of a pull request
    """
    # Create a new API link to get the reviews of a specific pull request
    pr_comments_reviews_url = pull_request['url'] + '/reviews'

    # Initialise empty list which will store all comments for a PR
    all_comments = []
    tasks = []

    # Recursive definition which retrieves all comments for a given URL    
    async def retrieve_comments(comment_url, type, session):
        """
        Recursively retrieves nested comments within a pull request.

        Parameters:
        comment_url (str): The URL to fetch comments from.
        type (str): The type of the comment (review, comment, or issue).
        session (aiohttp.ClientSession): The asynchronous session with the authentication headers included.
        """
        # Get all pagination urls to be able to get all comments
        comment_page_urls = await get_all_page_urls(session, comment_url)
        print("helloooo")
        print(comment_page_urls)
        # Create tasks to process each comment page concurrently
        comment_tasks = [asyncio.create_task(fetch_comment_page(session, url)) for url in comment_page_urls]
        # Wait until all tasks are complete
        comment_pages = await asyncio.gather(*comment_tasks)

        # Iterate over each response and add comments to the list
        for page in comment_pages:
            for comment in page:
                comment['comment_type'] = type
                all_comments.append(comment)
                print("doeii")
                if type == 'review API':
                    pr_nested_comment_url = pr_comments_reviews_url + f"/{comment['id']}/comments"
                    task = asyncio.create_task(retrieve_comments(pr_nested_comment_url, type, session))
                    tasks.append(task)

    # Retrieve comments from the reviews URL
    # This ensures that all review comments are added to all_comments.
    await retrieve_comments(pr_comments_reviews_url, 'review API', session),
    await asyncio.gather(*tasks)  # Await nested comment tasks

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
    try:
        async with session.get(url) as response:
            # Ensure that the response is succesful
            print("helppp")
            print(response)
            response.raise_for_status()
            print(response)
            # Create json object from response
            comments = await response.json()
            print(comments)
            # Return all comments on a single page
            return comments
    except aiohttp.ClientError as e:
        return []




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

    # Construct all page URLs concurrently by appending page numbers to the API call URL
    all_page_urls = [f'{pr_url}?page={page}' for page in range(1, total_pages + 1)]
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