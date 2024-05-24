import numpy as np

from .views import parse_Github_url_variables
from django.http import HttpResponse
from django.http import JsonResponse
from .nlp_functions import CodeCommitMessageRatio, FleschReadingEase, LexicalDensity
from .comment_info import list_of_comments
import asyncio

# Define and parse URL
#url = 'https://github.com/lucidrains/PaLM-rlhf-pytorch/pull/52/commits/297ac3e4c65f034de6ff3fa85008d871d6d786b2' #figure out how to set url from frontend
#url_parsed = parse_Github_url_variables(url)
#github_token = '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' #figure out how to import from settings.py
#headers = {'Authorization': f'token {github_token}'}

#repository_owner = url_parsed[1]
#repository_name = url_parsed[2]
#commit_sha = url_parsed[6]



# Comment list from list_of_comments function in comment_info. Used for testing average semantic score
# NOTE: displaying the list of comments
async def get_comments():
   comments = await list_of_comments()
   return comments

# list of all comments, awaits until get_comments() is complete
#comment_list = asyncio.run(get_comments())


# Retrieve all comments from get_comments until event loop is complete. 
# Related to the use of async in get_comments() function. 
# loop = asyncio.get_event_loop()
# comment_list = loop.run_until_complete(get_comments())


# Retrieve PyGithub commit object
#commitobject = CodeCommitMessageRatio.get_Github_commit_object(repository_owner, repository_name, commit_sha)


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
def calculate_weighted_commit_semantic_score(commitJSON, ld_weight, fre_weight, cmcl_weight, commit_url):
    # Get commit message in string form
    commit_message = commitJSON["commit"]["message"]
    print(commit_url)
    parsed_commit_url = parse_Github_url_variables(commit_url)
    print(parsed_commit_url)
    commit = CodeCommitMessageRatio.get_Github_commit_object(parsed_commit_url[2], parsed_commit_url[3], parsed_commit_url[-1])
    
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


# Function which calculates the weighted semantic score for comments.
# Separate function because commit/code ratio cannot be computed for comments.  
def calculate_weighted_comment_semantic_score(message, ld_weight, fre_weight):
   # Get Flesch reading ease value for message
    flesch_reading_ease = FleschReadingEase.calculate_flesch_reading_ease(message)
    weighted_flesch_reading_ease = fre_weight * flesch_reading_ease

    # Get lexical density value for message
    lexical_density = LexicalDensity.single_message_lexical_density(message)
    weighted_lexical_density = ld_weight * lexical_density

    total_weight = ld_weight + fre_weight

    # Return -1 if total weight is 0, else return weighted semantic score
    return (weighted_flesch_reading_ease+weighted_lexical_density)/total_weight if total_weight != 0 else -1
   

def calculate_average_weighted_comment_semantic_score(message_list, ld_weight, fre_weight):
   total_semantic_score = 0
   for message in message_list:
      total_semantic_score += calculate_weighted_comment_semantic_score(message,ld_weight,fre_weight)
    
   return total_semantic_score/len(message_list) if len(message_list) != 0 else -1

def displaySemantic(request):
#    return HttpResponse(calculate_weighted_semantic_score(commit,0,100,0))    
#    return HttpResponse(calculate_weighted_comment_semantic_score(comment_list[0],100,100))  #
   #return HttpResponse(calculate_average_weighted_comment_semantic_score(comment_list[1:10],1,100)) 
   return ""



# def displaySemantic(request):
#    return HttpResponse(calculate_semantic_score(commit))


# def dumpRatio(request):
#     commit = CodeCommitMessageRatio.get_Github_commit_object(repository_owner, repository_name, commit_sha, github_token)
#     commit_message = CodeCommitMessageRatio.get_commit_message(commit)
#     return HttpResponse(commit_message)










