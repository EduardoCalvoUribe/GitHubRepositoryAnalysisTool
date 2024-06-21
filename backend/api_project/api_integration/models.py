# Copyright 2024 Radboud University, Modern Software Development Techniques

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from django.utils import timezone
from django.db import models
from datetime import date

class User(models.Model): # user
    name = models.CharField(max_length=100)
    url = models.URLField()
    login = models.CharField(max_length=100, blank=True)
    repositories = models.JSONField(blank=True, default=list) # list of repos
    pull_requests = models.JSONField(blank=True, default=list) # list of pull requests
    comments = models.JSONField(blank=True, default=list) # list of comments
    commits = models.JSONField(blank=True, default=list) # list of commits

    def __str__(self):
        return self.login

    class Meta:
        app_label = 'api_integration'


class Repository(models.Model): # repository, might have to change this into comment
    name = models.CharField(max_length=100) # name of repository
    owner = models.CharField(max_length=100, default = "") # Ownver of the repository
    url = models.URLField() # api url of repository
    updated_at = models.DateTimeField(default=timezone.now) # time of last update in database
    #contributers = models.JSONField(blank=True, default=dict) # list of users
    pull_requests_list = models.JSONField(blank=True, default=list) # list of pull request in repository 
    commits_list = models.JSONField(blank=True, default=list) # list of commits in repository
    comments_list = models.JSONField(blank=True, default=list) # list of comments in repository
    users_list = models.JSONField(blank=True, default=list) # list of users in repository 
    token = models.CharField(max_length=100, default = "") # save personal access token
    average_semantic_score = models.FloatField(default=0.0) # average semantic score of the repository

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'api_integration'


class PullRequest(models.Model): # pull request
    repo = models.ForeignKey(Repository, related_name="pull_requests", on_delete=models.CASCADE, null=True, blank=True)
    url = models.URLField()
    updated_at = models.DateTimeField(default=timezone.now)
    closed_at = models.DateField(default=date.today)
    date = models.DateField(default=date.today)
    title = models.CharField(max_length=100)
    body = models.TextField(null=True, blank=True)
    user = models.CharField(max_length=100)
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.url
    
    class Meta:
        app_label = 'api_integration'
    

class Commit(models.Model): # commit
    pull_request = models.ForeignKey(PullRequest, related_name='commits', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    url = models.URLField()
    title = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    date = models.DateField(default=date.today)
    semantic_score = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(default=timezone.now)   

    def __str__(self):
        return self.name
    
    class Meta:
        app_label = 'api_integration'


class Comment(models.Model): # comment
    pull_request = models.ForeignKey(PullRequest, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    url = models.URLField() # API url of comment
    date = models.DateField(default=date.today) # Date of comment
    updated_at = models.DateTimeField(default=timezone.now) # Date last updated in database
    body = models.CharField(max_length=500,null=True,blank=True) # Body of comment
    user = models.CharField(max_length=100) # User that posted the comment
    semantic_score = models.FloatField(default=0.0)
    comment_type = models.CharField(max_length=200, default= "")
    commit_id = models.CharField(max_length=200, default = "")

    def __str__(self):
        return self.url

    class Meta:
        app_label = 'api_integration'
