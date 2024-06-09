import numpy as np

from . import views
from django.http import HttpResponse
from django.http import JsonResponse
from .nlp_functions import FleschReadingEase, LexicalDensity, AsyncCodeCommitMessageRatio
# from .comment_info import list_of_comments
import asyncio

# Sigmoid helper function used for bounding commit message/code ratio value between 0 and 100
def sigmoid(x):
 return (1/(1 + np.exp(-x)))*100

# NOTE: redundant function, use calculateWeightedCommitSemanticScore instead. 
# Function which calculates the semantic score with every metric weighted equally
# In order to retrieve message from commit object, let commit_message = commit.commit.message
# def calculateSemanticScore(commit):
#     # Get commit message associated with commit object in string form
#     commit_message = commit.commit.message
    
#     # Get commit message/code length ratio, bounded between 0 and 1 by sigmoid function
#     bounded_ratio = sigmoid(CodeCommitMessageRatio.computeCodeCommitRatio(commit))

#     # Get Flesch reading ease value for commit message
#     flesch_reading_ease = FleschReadingEase.calculateFleschReadingEase(commit_message)

#     # Get lexical density value for commit message
#     lexical_density = LexicalDensity.singleMessageLexicalDensity(commit_message)

#     return (bounded_ratio + flesch_reading_ease + lexical_density)/3

# Function which calculates the semantic score with adjusted weights
# Accepts additional parameters ld_weight, fre_weight and cmcl_weight, representing the weights
# for lexical density, Flesch reading ease and commit message length/code length ratio respectively.
# In order to retrieve message from commit object, let commit_message = commit.commit.message
async def calculateWeightedCommitSemanticScore(commitJSON, ld_weight, fre_weight, cmcl_weight, commit_url, pr_num):
    # Get commit message in string form
    commit_message = commitJSON["commit"]["message"]

    # Parse relevant variables for code/commit message ratio function
    parsed_commit_url = views.parse_Github_url_variables(commit_url)
    owner = parsed_commit_url[2]
    repo = parsed_commit_url[3]
    commit_SHA = parsed_commit_url[-1]
    
    awaited_bounded_ratio = await AsyncCodeCommitMessageRatio.compute_code_commit_ratio(owner,repo,pr_num,commit_SHA)
    bounded_ratio = sigmoid(awaited_bounded_ratio)
    weighted_bounded_ratio = cmcl_weight * bounded_ratio


    #commit = CodeCommitMessageRatio.getGithubCommitObject(parsed_commit_url[2], parsed_commit_url[3], parsed_commit_url[-1])
    
    # Get commit message/code length ratio, bounded between 0 and 1 by sigmoid function
    #bounded_ratio = sigmoid(CodeCommitMessageRatio.computeCodeCommitRatio(commit))
    #weighted_bounded_ratio = cmcl_weight * bounded_ratio

    # Get Flesch reading ease value for commit message
    flesch_reading_ease = FleschReadingEase.calculateFleschReadingEase(commit_message)
    weighted_flesch_reading_ease = fre_weight * flesch_reading_ease

    # Get lexical density value for commit message
    lexical_density = LexicalDensity.singleMessageLexicalDensity(commit_message)
    weighted_lexical_density = ld_weight * lexical_density

    total_weight = ld_weight + fre_weight + cmcl_weight

    # Return -1 if total weight is 0, else return weighted semantic score
   #  return (weighted_flesch_reading_ease+weighted_lexical_density)/total_weight if total_weight != 0 else -1

    return (weighted_bounded_ratio+weighted_flesch_reading_ease+weighted_lexical_density)/total_weight if total_weight != 0 else -1


# Function which calculates the weighted semantic score for comments.
# Separate function because commit/code ratio cannot be computed for comments.  
def calculateWeightedCommentSemanticScore(message, ld_weight, fre_weight):
   # Get Flesch reading ease value for message
    flesch_reading_ease = FleschReadingEase.calculateFleschReadingEase(message)
    weighted_flesch_reading_ease = fre_weight * flesch_reading_ease

    # Get lexical density value for message
    lexical_density = LexicalDensity.singleMessageLexicalDensity(message)
    weighted_lexical_density = ld_weight * lexical_density

    total_weight = ld_weight + fre_weight

    # Return -1 if total weight is 0, else return weighted semantic score
    return (weighted_flesch_reading_ease+weighted_lexical_density)/total_weight if total_weight != 0 else -1
   
# Function which calculates the average weighted semantic score for a list of comments.
# NOTE: this function might be redundant due to database.
def calculateAverageWeightedCommentSemanticScore(message_list, ld_weight, fre_weight):
   total_semantic_score = 0
   for message in message_list:
      total_semantic_score += calculateWeightedCommentSemanticScore(message,ld_weight,fre_weight)
    
   return total_semantic_score/len(message_list) if len(message_list) != 0 else -1








