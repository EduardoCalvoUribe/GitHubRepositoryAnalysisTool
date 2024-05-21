import numpy as np

from .views import parse_Github_url_variables
from django.http import HttpResponse
from .nlp_functions import CodeCommitMessageRatio, FleschReadingEase, LexicalDensity
from .comment_info import list_of_comments

# Define and parse URL
url = 'https://github.com/lucidrains/PaLM-rlhf-pytorch/pull/52/commits/297ac3e4c65f034de6ff3fa85008d871d6d786b2' #figure out how to set url from frontend
url_parsed = parse_Github_url_variables(url)
github_token = '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' #figure out how to import from settings.py
headers = {'Authorization': f'token {github_token}'}

repository_owner = url_parsed[1]
repository_name = url_parsed[2]
commit_sha = url_parsed[6]


# Comment list from list_of_comments function in comment_info. Used for testing average semantic score
# NOTE: displaying the list of comments
async def get_comments(request):
   comments = await list_of_comments()
   return comments


# Retrieve PyGithub commit object
commit = CodeCommitMessageRatio.get_Github_commit_object(repository_owner, repository_name, commit_sha, github_token)


# Sigmoid function used for bounding commit message/code ratio value between 0 and 100
def sigmoid(x):
 return (1/(1 + np.exp(-x)))*100

# Function which calculates the semantic score with every metric weighted equally
# In order to retrieve message from commit object, let commit_message = commit.commit.message
def calculate_semantic_score(commit):
    # Get commit message associated with commit object in string form
    commit_message = commit.commit.message
    
    # Get commit message/code length ratio, bounded between 0 and 1 by sigmoid function
    bounded_ratio = sigmoid(CodeCommitMessageRatio.compute_code_commit_ratio(commit))

    # Get Flesch reading ease value for commit message
    flesch_reading_ease = FleschReadingEase.calculate_flesch_reading_ease(commit_message)

    # Get lexical density value for commit message
    lexical_density = LexicalDensity.single_message_lexical_density(commit_message)

    return (bounded_ratio + flesch_reading_ease + lexical_density)/3

# Function which calculates the semantic score with adjusted weights
# Accepts additional parameters ld_weight, fre_weight and cmcl_weight, representing the weights
# for lexical density, Flesch reading ease and commit message length/code length ratio respectively.
# In order to retrieve message from commit object, let commit_message = commit.commit.message
def calculate_weighted_semantic_score(commit, ld_weight, fre_weight, cmcl_weight):
    # Get commit message in string form
    commit_message = commit.commit.message
    
    # Get commit message/code length ratio, bounded between 0 and 1 by sigmoid function
    bounded_ratio = sigmoid(CodeCommitMessageRatio.compute_code_commit_ratio(commit))
    weighted_bounded_ratio = cmcl_weight * bounded_ratio

    # Get Flesch reading ease value for commit message
    flesch_reading_ease = FleschReadingEase.calculate_flesch_reading_ease(commit_message)
    weighted_flesch_reading_ease = fre_weight * flesch_reading_ease

    # Get lexical density value for commit message
    lexical_density = LexicalDensity.single_message_lexical_density(commit_message)
    weighted_lexical_density = ld_weight * lexical_density

    total_weight = ld_weight + fre_weight + cmcl_weight

    # Return -1 if total weight is 0, else return weighted semantic score
    return (weighted_bounded_ratio+weighted_flesch_reading_ease+weighted_lexical_density)/total_weight if total_weight != 0 else -1


   


def displaySemantic(request):
   return HttpResponse(calculate_weighted_semantic_score(commit,0,100,0))    



# def displaySemantic(request):
#    return HttpResponse(calculate_semantic_score(commit))


# def dumpRatio(request):
#     commit = CodeCommitMessageRatio.get_Github_commit_object(repository_owner, repository_name, commit_sha, github_token)
#     commit_message = CodeCommitMessageRatio.get_commit_message(commit)
#     return HttpResponse(commit_message)










