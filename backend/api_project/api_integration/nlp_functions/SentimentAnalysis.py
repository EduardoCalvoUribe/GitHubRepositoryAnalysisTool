# Copyright 2024 Radboud University, Modern Software Development Techniques

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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




        