from django.http import JsonResponse
from django.utils import timezone
from django.db import models
from . import functions

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
    users = models.JSONField(blank=True, default=dict) 

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
                        setattr(repo, key, value)
                    else:
                        setattr(repo, key, "")
            setattr(repo, "users", functions.pull_request_per_user()) # update users
            repo.save()
        except Exception as e:
            return JsonResponse({"error": str(e)})

    class Meta:
        app_label = 'api_integration'