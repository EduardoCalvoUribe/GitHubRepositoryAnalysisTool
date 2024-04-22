# TO ADD (minor bug solving): This function does not yet properly handle URLs, for instance the string "github.com" currently gets 
# a low Flesch reading ease score way below 0. Furthermore, the output for standalone words (so a string containing only 1 word)
# which are unknown to cmudict get Flesch reading ease scores which vary highly, often being either 36, 121 or way below 0. 
# Furthermore, decide if negative Flesch reading ease scores should be set as 0 to have clearly defined bounds for semantic score.

# NOTE: for this function, the nltk dependency must be installed (pip install nltk)
import nltk

# download cmudict
nltk.download('cmudict')
#import cmudict (pronounciation dictionary) for annotated syllables
from nltk.corpus import cmudict
# read in cmudict as dictionary
d = cmudict.dict()

# Sentence count using nltk sent_tokenize
nltk.download('punkt')
from nltk.tokenize import sent_tokenize


#Function which calculates the Flesch reading ease metric for a given message.
#Returns Flesch reading ease as a single numerical value
def calculate_flesch_reading_ease(message):
    # Count number of words with .split() function. By default the separator character is any whitespace
    wordCount = len(message.split())
    # Count sentences using nltk sent_tokenize
    sentenceCount = len(sent_tokenize(message))
    # Initialise syllable count for message using syllable_count function.
    syllableCount = 0

    # Count total syllable count
    for word in message.split():
        syllableCount += syllable_count(word)
    
    # Calculate Flesch reading ease score with the associated formula
    # Initialise Flesch reading ease score as 0 
    flesch_reading_ease_score = 0

    # If wordCount or sentenceCount are 0, let Flesch reading ease score be 
    # out of bounds (max Flesch reading ease score is around 121) due to undefined division by 0
    if (sentenceCount == 0 or wordCount == 0):
        flesch_reading_ease_score = 1000
    else:
    # else calculate Flesch reading ease score
        flesch_reading_ease_score = 206.835 - (1.015 * (wordCount/sentenceCount)) - (84.6 * (syllableCount/wordCount))

    # Return Flesch reading ease score.
    # If Flesch reading ease score is 1000, then an undefined division by 0 has occurred. 
    return flesch_reading_ease_score 


    # Code for future reference, might be relevant if lower bound for Flesch reading ease score is set to 0.
    # if flesch_reading_ease_score > 0:
    #     return flesch_reading_ease_score
    # # Else if Flesch reading ease score is 0, return 0.
    # elif flesch_reading_ease_score == 0:
    #     return 0
    # # Return -1 if sentenceCount = 0 or wordCount = 0 (undefined division by 0 in formula)
    # elif flesch_reading_ease_score < 0:
    #     return -1

#Helper function which checks if word is in cmudict dictionary.
def lookup_word(word):
    return d.get(word)

# Function which uses cmudict to return number of syllables, if word not in cmudict then number of syllables is counted manually. 
# Courtesy of https://datascience.stackexchange.com/questions/23376/how-to-get-the-number-of-syllables-in-a-word
def syllable_count(word):
    wordCheck = lookup_word(word)

    #if wordCheck is not empty and therefore word is in dictionary
    if wordCheck:
        # Process first matched word in dictionary
        wordForProcessing = wordCheck[0]
        return len([p for p in wordForProcessing if p[-1].isdigit()])
    # else if word not found in cmudict
    else:        
        return otherSyllables(word)

# Function with simple heuristic for determining the number of syllables in English words. 
# All words which are not in cmudict are processed by this function. 
# Courtesy of https://datascience.stackexchange.com/questions/23376/how-to-get-the-number-of-syllables-in-a-word, 
# slightly adjusted and improved by ChatGPT 3.5. 
def otherSyllables(word):
    # syllable count
    count = 0

    vowels = 'aeiouy'
    word = word.lower()
    if word[0] in vowels:
        count += 1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count += 1

    # Handling common suffixes/prefixes
    if word.endswith(('es', 'ed')):
        count -= 1
    elif word.endswith('ly'):
        # Consider 'ly' as a single syllable in most cases
        count = max(count - 1, 1)

    # Handling exceptions
    if word.endswith('e'):
        # Drop silent 'e' at the end
        count -= 1
        if word.endswith('le'):
            count += 1
    
    # Avoid counting 0 syllables
    return max(count, 1)

# This function computes the average flesch reading ease for a list of message strings. messageList must be a list of strings.
# NOTE: The average flesch reading ease score can also be calculated with aggregate avg() function in sqlite database. 
# However, this is only possible if we decide to store the flesch reading ease scores in the database. 
def calculate_average_flesch_reading_ease(messageList):
  # Initialise total flesch reading ease variable
  total_flesch_reading_ease = 0
  
  # Sum all flesch reading eases for every message in messageList
  for message in messageList:
    total_flesch_reading_ease += calculate_flesch_reading_ease(message)

  # Return average flesch reading ease by dividing total flesch reading ease by length of messageList
  return total_flesch_reading_ease/len(messageList)
