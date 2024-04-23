# Required dependencies to be installed for sentiment analysis in our webapp.
# Note that the sentiment analysis metric will integrate the Vader and the TextBlob libraries

# TextBlob:
# !pip install textblob
from textblob import TextBlob

# Vader:
#!pip install nltk
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# This function accepts a list of strings. For this list of strings, 
# a TextBlob-based average sentiment analysis score ranging from -1 to 1 is returned.
# A score of -1 indicates a negative sentiment, whereas a score of 1 indicates a positive sentiment.
# NOTE: message_list should not be empty

def textBlobSA(message_list):
    # Throw exception if length of message_list is 0.
    if len(message_list) == 0:
        raise ValueError("length of message_list must be larger than 0.")

    # initialise empty list which will contain sentiment polarity and subjectivity scores
    sentiment_list = []
    # initialise total sentiment score
    total_sentiment_score = 0

    # loop over all messages in messageList
    for message in message_list:
        # apply TextBlob sentiment analysis on message
        tb_message = TextBlob(message).sentiment       
        sentiment_list.append(tb_message)
        # add sentiment polarity score to total_sentiment_score
        total_sentiment_score += tb_message[0]

    # calculate average sentiment score
    avg_sentiment = total_sentiment_score/len(sentiment_list)

    # Return list of sentiment analysis scores and the average sentiment score.
    return sentiment_list,avg_sentiment

# This function accepts a list of strings. For this list of strings, 
# an average sentiment analysis score ranging from -1 to 1 is returned.
# A score of -1 indicates a negative sentiment, whereas a score of 1 indicates a positive sentiment.
# NOTE: message_list should not be empty
def vaderSA(message_list):
    # Throw exception if length of message_list is 0.
    if len(message_list) == 0:
        raise ValueError("length of message_list must be larger than 0.")
    
    # Initialise empty list which will contain sentiment polarities
    # available sentiment polarities are 'neg','neu','pos' and 'compound'.
    sentiment_list = []

    # initialise total sentiment score
    total_sentiment_score = 0

    # Initialise SentimentIntensityAnalyzer. Variable name sia is an abbreviation
    sia = SentimentIntensityAnalyzer()

    # loop over all messages in messageList
    for message in message_list:
        # apply Vader sentiment analysis on message
        sa_scores = sia.polarity_scores(message)
        sentiment_list.append(sa_scores)
        # add compound sentiment analysis score for message to total_sentiment_score
        total_sentiment_score += sa_scores['compound']
    
    # calculate average sentiment score consisting of total compound sentiment analysis scores
    avg_sentiment = total_sentiment_score/len(sentiment_list)

    # Return list of sentiment analysis scores and the average sentiment score.
    return sentiment_list,avg_sentiment




        