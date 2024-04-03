from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.conf import settings
from datetime import datetime
from collections import Counter
from . import functions

def repo_total_commits(request, owner, repo, pull_number, start_date, end_date, status, set):
    # TODO: What should the final reponse be to be able to be used by frontend
    # start/end_date = YYYY-MM-DD
    # status = open, closed or all
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
            pull_text_to_display, pull_total_commit_amount, pull_user_commit_count = pull_commits(request, owner, repo, pull_number, start_date, end_date, status)
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
    return HttpResponse(text_to_display_neat)


def general_repo_commits(request, owner, repo, start_date, end_date):
    # API call for the commits not associated to a PR
    repo_commits_url = f'https://api.github.com/repos/{owner}/{repo}/commits?since={start_date}&until={end_date}'

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

def pull_commits(request, owner, repo, pull_number, start_date, end_date, status):
    text_to_display = ""
    total_commit_amount = 0
    user_commit_count = {}

    pr_commits_url = f'https://api.github.com/repos/{owner}/{repo}/pulls?state={status}'
    # As long as there are other pages the loop should keep running
    while pr_commits_url:
        pr_response = functions.get_api_reponse(pr_commits_url)
        pull_requests = pr_response.json()
        
        # Filter all the pull request to only get those that have been updated in between the given start and end date
        filtered_pull_requests = [pr for pr in pull_requests if start_date <= pr['updated_at'] <= end_date]
        
        # Iterate over pull requests to fetch commits associated with each pull request
        for pull_request in filtered_pull_requests:
            # Get new API call request for the commits of a pull request
            pull_request_commits_url = pull_request['commits_url'].replace("{/sha}", "")
            print(pull_request_commits_url) # Used to check how many API calls are made
            
            pr_commits_response = functions.get_api_reponse(pull_request_commits_url)
            pr_commits = pr_commits_response.json()

            # Iterate over commits associated with the pull request
            for commit in pr_commits:
                commit_date = datetime.strptime(commit['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ").isoformat()
                # Only show the commits done in the speficic time frame
                if start_date <= commit_date <= end_date:
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
                    text_to_display += "<p><b>Pull Request</b>: " + f"Pull Request #{pull_request['number']}: {pull_request['title']}" + "</p>"
                    text_to_display += "<p><b>Message</b>: " + commit_message + "</p>"
            
        if ('next' in pr_response.links) and not (filtered_pull_requests==[]):
            pr_commits_url = pr_response.links['next']['url']
        else:
            pr_commits_url = None

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