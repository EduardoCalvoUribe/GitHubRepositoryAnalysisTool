"""
This file contains the functions which are responsible for computing the general semantic score
"""
import numpy as np
from . import views
from .nlp_functions import FleschReadingEase, LexicalDensity, AsyncCodeCommitMessageRatio


def sigmoid(x):
    """
    Helper function which bounds code/commit message ratio value between 0 and 100 using a sigmoid.
    
    Parameters:
    x: The float value which is passed to the sigmoid function.

    Returns:
    float: A float between 0 and 100 representing bounded code/commit message ratio.
    """
    return (1/(1 + np.exp(-x)))*100

async def calculateWeightedCommitSemanticScore(commitJSON, ld_weight, fre_weight, cmcl_weight, commit_url, pr_num):
    """
    Function which calculates the weighted general semantic score
    for the commit message associated with a commit object.

    In this function, the following metrics are integrated: Flesch reading ease, 
    lexical density, code/commit message ratio

    This function is used in the commit_task function in API_call_information.py, 
    since the semantic score is calculated for a commit message and subsequently added
    to the database as a part of the commit object. 
    
    Currently, the weights are defined within the commit_task function.
    NOTE: TO ADD: Specify weights in frontend and pass them to from frontend all the 
    way to this function. TO ADD: Check in frontend that weights are > 0 (non-negative
    and not equal to 0)
    
    Parameters:
    commitJSON: A JSON commit object which contains the commit message for which the semantic score is calculated
    ld_weight: Numerical value which represents the importance weight for the lexical density metric
    fre_weight: Numerical value which represents the importance weight for the Flesch reading ease metric
    cmcl_weight: Numerical value which represents the importance weight for the code/commit message ratio metric
    commit_url: String which represents the URL associated with the commit for which the semantic score is calculated
    pr_num: Integer which represents the number of the pull request which the commit is a part of 

    Returns:
    float: A float between 0 and 100 representing the (weighted) semantic score for 
    a commit message.
    """
 
    # Retrieve commit message in string form from the commitJSON object
    commit_message = commitJSON["commit"]["message"]

    # Parse relevant variables for code/commit message ratio function
    parsed_commit_url = views.parse_Github_url_variables(commit_url)
    owner = parsed_commit_url[2]
    repo = parsed_commit_url[3]
    commit_SHA = parsed_commit_url[-1]
    

    
    """
    NOTE: This is the code for computing the code/commit message ratio. To include it in the semantic score, 
    please ensure that the variables within these multiline comment are uncommented. Furthermore, please ensure
    that the steps as documented for total_weight and the return statement within this function are followed correctly. 

    # Asynchronously compute code/commit message ratio. Await result
    awaited_bounded_ratio = await AsyncCodeCommitMessageRatio.compute_code_commit_ratio(owner,repo,pr_num,commit_SHA,commitJSON)
    bounded_ratio = sigmoid(awaited_bounded_ratio)
    # Multiply metric with its respective weight
    weighted_bounded_ratio = cmcl_weight * bounded_ratio
    """

    # Get Flesch reading ease value for commit message
    flesch_reading_ease = FleschReadingEase.calculateFleschReadingEase(commit_message)
    # Multiply metric with its respective weight
    weighted_flesch_reading_ease = fre_weight * flesch_reading_ease

    # Get lexical density value for commit message
    lexical_density = LexicalDensity.singleMessageLexicalDensity(commit_message)
    # Multiply metric with its respective weight
    weighted_lexical_density = ld_weight * lexical_density

    # Sum up all weights
    # NOTE: Add cmcl_weight if code/commit message ratio should be included in semantic score.
    total_weight = ld_weight + fre_weight 

    # NOTE: Add weighted_bounded_ratio to the return statement if commit message length/code length ratio should be 
    # in semantic score. 
    return (weighted_flesch_reading_ease+weighted_lexical_density)/total_weight if total_weight != 0 else -1


# Function which calculates the weighted semantic score for comments.
# Separate function because commit/code ratio cannot be computed for comments.  
def calculateWeightedCommentSemanticScore(message, ld_weight, fre_weight):
    """
    Function which calculates the weighted general semantic score for a comment message.

    In this function, the following metrics are integrated: Flesch reading ease, 
    lexical density

    This function is used in the comment_task function in API_call_information.py, 
    since the semantic score is calculated for a comment message and subsequently added
    to the database as a part of the comment object. 
    
    Currently, the weights are defined within the comment_task function.
    NOTE: TO ADD: Specify weights in frontend and pass them to from frontend all the 
    way to this function. TO ADD: Check in frontend that weights are > 0 (non-negative
    and not equal to 0)
    
    Parameters:
    message: String for which the semantic score is calculated
    ld_weight: Numerical value which represents the importance weight for the lexical density metric
    fre_weight: Numerical value which represents the importance weight for the Flesch reading ease metric

    Returns:
    float: A float between 0 and 100 representing the (weighted) semantic score for 
    a comment message.
    """
 
    # Get Flesch reading ease value for comment message
    flesch_reading_ease = FleschReadingEase.calculateFleschReadingEase(message)
    # Multiply metric with its respective weight
    weighted_flesch_reading_ease = fre_weight * flesch_reading_ease

    # Get lexical density value for comment message
    lexical_density = LexicalDensity.singleMessageLexicalDensity(message)
    # Multiply metric with its respective weight
    weighted_lexical_density = ld_weight * lexical_density

    # Sum up all weights
    total_weight = ld_weight + fre_weight

    # Return -1 if total weight is 0, else return weighted semantic score
    return (weighted_flesch_reading_ease+weighted_lexical_density)/total_weight if total_weight != 0 else -1
