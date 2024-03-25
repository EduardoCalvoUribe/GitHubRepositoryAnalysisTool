from django.http import JsonResponse
from django.utils import timezone
from django.db import models
#from .functions import *

class Users(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    updated_at = timezone.now()
    login = models.CharField(max_length=100, blank=True)
    avatar_url = models.URLField(blank=True)

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


class Repos(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    updated_at = timezone.now()
    login = models.CharField(max_length=100, blank=True)
    avatar_url = models.URLField(blank=True)
    #users = pull_request_per_user

    def __str__(self):
        return self.name
    
    @classmethod
    def save_repo_to_db(request, json_response):
        try:
        # Convert API response to JSON format
            repo = Repos()

            for key,value in json_response.items():
                if key is not None:
                    if value is not None:
                        setattr(repo, key, value)
                    else:
                        setattr(repo, key, "")

            repo.save()
        except Exception as e:
            return JsonResponse({"error": str(e)})

    class Meta:
        app_label = 'api_integration'