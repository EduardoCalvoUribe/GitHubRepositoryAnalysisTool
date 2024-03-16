from django.utils import timezone
from django.db import models

class Users(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    updated_at = timezone.now()
    login = models.CharField(max_length=100, blank=True)
    avatar_url = models.URLField(blank=True)

    def __str__(self):
        return self.name
    class Meta:
        app_label = 'api_integration'


class Repos(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    updated_at = timezone.now()
    login = models.CharField(max_length=100, blank=True)
    avatar_url = models.URLField(blank=True)

    def __str__(self):
        return self.name
    class Meta:
        app_label = 'api_integration'