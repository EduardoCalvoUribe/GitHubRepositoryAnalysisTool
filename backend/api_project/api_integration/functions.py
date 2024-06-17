from django.conf import settings
from django.http import JsonResponse
import requests
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


def get_api_reponse(URL):
    """
    Sends a GET request to the specified URL with the provided personal access token.

    Args:
        URL (str): The URL to send the GET request to.

    Returns:
        requests.Response: The response object containing the API response.

    Raises:
        None

    """
    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    #personal_access_token = get_personal_access_token(URL) # commented because other functions are not implemented yet
    headers = {'Authorization': f'token {personal_access_token}'}
    api_response = requests.get(URL, headers=headers)
    return api_response
