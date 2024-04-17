from django.conf import settings
from django.http import JsonResponse
import requests


def get_api_reponse(URL):
    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    headers = {'Authorization': f'token {personal_access_token}'}
    api_response = requests.get(URL, headers=headers)
    return api_response


def pull_request_per_user(self):
    url = 'https://api.github.com/repos/django/django/pulls'
    # Make the GET request to the GitHub API
    api_response = get_api_reponse(url).json()
    id_counts = {}  # Dictionary to store the counts for each 'id'

    # Iterate over each item in the API response
    for item in api_response:
        user_id = item.get('user', {}).get('id')  # Get the 'id' value from the dictionary
        user_login = item.get('user', {}).get('login')  # Get the 'login' value from the dictionary
        key = "{}({})".format(user_id,user_login) # create a string which makes user id and value the key
        if user_id:
            id_counts[key] = id_counts.get(key, 0) + 1  # Increment the count for the 'id'

    sorted_user_count_dict = dict(sorted(id_counts.items(), key=lambda x: x[1], reverse=True)) # create a sorted by value dictionary of the user_id's
    return sorted_user_count_dict

