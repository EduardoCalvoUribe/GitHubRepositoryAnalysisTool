from django.http import JsonResponse
from django.utils import timezone
from django.db import models
from . import functions

class Users(models.Model): # user
    name = models.CharField(max_length=100)
    url = models.URLField()
    login = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
    
    @classmethod
    def save_user_to_db(request, json_response):
        try:
            # Convert API response to JSON format
            user = Users()

            for key,value in json_response.items():
                if key is not None:
                    if value is not None:
                        setattr(user, key, value)
                    else:
                        setattr(user, key, "")

            user.save()
            data = list(Users.objects.values())
            return JsonResponse({'data': data})
        except Exception as e:
            return JsonResponse({"error": str(e)})

    class Meta:
        app_label = 'api_integration'


class Repos(models.Model): # repository, might have to change this into comment
    name = models.CharField(max_length=100) # name of repository
    url = models.URLField() # api url of repository
    updated_at = timezone.now() # time of last update
    contributers = models.JSONField(blank=True, default=dict) # list of amount of pull request per users
    pull_requests = models.JSONField(blank=True, default=dict) # list of pull request in repository
    token = models.CharField(max_length=100) # save personal access token

    def __str__(self):
        return self.name
    
    @classmethod
    def save_repo_to_db(self, json_response):
        try:
        # Convert API response to JSON format
            repo = Repos()
            for key,value in json_response.items():
                if key is not None:
                    if value is not None:
                        if "_url" in key or "_url" in value:
                            setattr(repo, key, {'a':1})
                        else:
                            setattr(repo, key, value)
                    else:
                        setattr(repo, key, "")

            setattr(repo, "contributers", functions.pull_request_per_user()) # update users
            setattr(repo, "pull_requests", {"a":1})
            repo.save()
        except Exception as e:
            return JsonResponse({"error": str(e)})
        
    @classmethod
    def update_repo_in_db(self, json_response, repo, token):
        try:
        # Convert API response to JSON format
            for key,value in json_response.items():
                if key is not None:
                    if value is not None:
                        if "_url" in key or "_url" in value:
                            setattr(repo, key, {'a':1})
                        else:
                            setattr(repo, key, value)
                    else:
                        setattr(repo, key, "")
            setattr(repo, "contributers", functions.pull_request_per_user()) # update users
            setattr(repo, "pull_requests", {"a":1})
            setattr(repo, "token", token)
            repo.save()
        except Exception as e:
            return JsonResponse({"error": str(e)})

    class Meta:
        app_label = 'api_integration'

class PullRequest(models.Model): # pull request
    name = models.CharField(max_length=100)
    url = models.URLField()
    updated_at = timezone.now()
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    comments = models.JSONField(blank=True, default=dict)
    #closed = model.

    def __str__(self):
        return self.name
    
    @classmethod
    def save_pull_to_db(request, json_response):
        try:
            # Convert API response to JSON format
            pull_request = PullRequest()

            for key,value in json_response.items():
                if key is not None:
                    if value is not None:
                        setattr(pull_request, key, value)
                    else:
                        setattr(pull_request, key, "")

            pull_request.save()
            data = list(pull_request.objects.values())
            return JsonResponse({'data': data})
        except Exception as e:
            return JsonResponse({"error": str(e)})

    class Meta:
        app_label = 'api_integration'


class Commit(models.Model): # commit
    name = models.CharField(max_length=100)
    url = models.URLField()
    date = models.DateField()
    updated_at = timezone.now()
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=500)
    user = models.CharField(max_length=100)
    comments = models.JSONField(blank=True, default=dict)

    def __str__(self):
        return self.name
    
    @classmethod
    def save_commit_to_db(request, commit_response):
        try:
            # Convert API response to JSON format
            commit = Commit()

            for key,value in commit_response.items():
                if key is not None:
                    if value is not None:
                        setattr(commit, key, value)
                    else:
                        setattr(commit, key, "")
            
            setattr(commit, "name", commit_response['commit']['message'])
            setattr(commit, "url", commit_response['commit']['url'])
            setattr(commit, "date", commit_response['commit']['author']['date'])
            setattr(commit, "title", commit_response['commit']['message'])
            setattr(commit, "body", '')
            setattr(commit, "user", commit_response['author']['login'])
            setattr(commit, "comments", '')

            commit.save()
            data = list(commit.objects.values())
            return JsonResponse({'data': data})
        except Exception as e:
            return JsonResponse({"error": str(e)})

    class Meta:
        app_label = 'api_integration'