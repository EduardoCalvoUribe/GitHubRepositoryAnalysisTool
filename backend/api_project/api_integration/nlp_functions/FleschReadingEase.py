# Necessary imports for FleschReadingEase.py
import nltk
from nltk.corpus import cmudict #Pronounciation dictionary for annotated syllables
from nltk.tokenize import sent_tokenize #Sentence count using sent_tokenize

# A list of libraries which must be installed manually, as explained in project report.
# If libraries are downloaded, please comment them out.
# nltk.download('cmudict') 
# nltk.download('punkt')

# Read in cmudict as dictionary
d = cmudict.dict()


#Function which calculates the Flesch reading ease metric for a given message.
#Returns Flesch reading ease as a single numerical value
# If division by 0 occurs -1 is returned.
def calculateFleschReadingEase(message):
    """
    Function which calculates the Flesch reading ease for a given message. This 
    metric is part of the general semantic score for commit and comment messages.

    The Flesch reading ease is a measure which measures the readability of a text fragment.
    The Flesch reading ease is dependent on the number of words in a message, 
    the number of sentences in a message and the number of syllables in a message.    

    The formula associated with the Flesch reading ease metric can be found on
    https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests

    In theory the Flesch reading ease value for a string can be negative (highly unreadable text),
    but this is uncommon. This function  ensures that the value is bounded between 0 and 100. 
    
    Parameters:
    message: The message for which the Flesch reading ease is computed. Must be a string.

    Returns:
    float: A float between 0 and 100 representing the (bounded) Flesch reading ease. 
    If message is None (not defined) or empty, the Flesch reading ease is set to 0. 
    """

    # If message is None type (not defined) or empty, let Flesch reading ease equal 0
    if message is None or message.strip() == "":
        return 0

    # Count number of words with .split() function. By default the separator character is any whitespace
    wordCount = len(message.split())

    # Count number of sentences using nltk sent_tokenize
    sentence_count = len(sent_tokenize(message))

    # Initialise syllable count for message using syllable_count function.
    syllable_count = 0

    # Count total syllable count
    for word in message.split():
        syllable_count += syllableCount(word)
    
    # If sentenceCount or wordCount are 0, return -1 to prevent division by 0
    if sentence_count == 0 or wordCount == 0:
        return -1
    
    # Calculate Flesch reading ease score
    flesch_reading_ease_score = 206.835 - (1.015 * (wordCount / sentence_count)) - (84.6 * (syllable_count / wordCount))

    # Bound the Flesch reading ease score between 0 and 100
    flesch_reading_ease_score = max(0, min(flesch_reading_ease_score, 100))

    # Return Flesch reading ease score.  
    return flesch_reading_ease_score 

def lookupWord(word):
    """
    Helper function which looks up word in cmudict dictionary.

    Parameters:
    word: The word which is looked up in cmudict dictionary.

    Returns:
    list object: A list object containing all matching phonetic representations for the word.    
    If no matching phonetic representations are found, the returned list is empty.
    """
    return d.get(word)

def syllableCount(word):
    """
    Function which returns the number of syllables in a word.

    This function uses cmudict to return the number of syllables for a word.
    If the word is not in the cmudict dictionary, then the number of syllables
    is counted manually. For a more detailed explanation on the manual syllable
    count, see documentation in the otherSyllables(word) function.

    Parameters:
    word: The word for which the number of syllables is returned. 

    Returns:
    int: The syllable count for the provided word.
    """

    # Look up word in cmudict dictionary
    wordCheck = lookupWord(word)

    #if wordCheck is not empty and therefore word is in dictionary
    if wordCheck:
        # Process first matched word in dictionary
        wordForProcessing = wordCheck[0]
        # Return number of syllables for the word
        return len([p for p in wordForProcessing if p[-1].isdigit()])
    # else if word not found in cmudict
    else:        
        # Return manually counted number of syllables for the word
        return otherSyllables(word)


def otherSyllables(word):
    """
    Function which manually counts the number of syllables in a word.

    This function counts the number of syllables manually for all words which 
    are not found in the cmudict dictionary. To count the number of syllables manually, 
    a heuristic has been used based on the linguistic heuristic as introduced in 
    https://datascience.stackexchange.com/questions/23376/how-to-get-the-number-of-syllables-in-a-word
    (and https://medium.com/@mholtzscher/programmatically-counting-syllables-ca760435fab4). 
    The heuristic has been slightly adjusted and improved by ChatGPT 3.5. The function 
    is used in the syllableCount function. 

    NOTE: the manual syllable count is not optimal and can be optimized in the future.  

    Parameters:
    word: The word for which the number of syllables is manually counted. 

    Returns:
    int: The syllable count for the provided word.
    """
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
def calculateAverageFleschReadingEase(messageList):
  """
    Function which computes the average Flesch reading ease for a list of message strings.

    NOTE: The same task can be easily done with the aggregate avg() function on data
    which is stored in the system database (db.sqlite3). This function may be relevant
    for data which is not stored in the database.

    Parameters:
    messageList: The list of messages for which the average Flesch reading ease
    is computed. Must be a list of strings. 

    Returns:
    float: A float between 0 and 100 representing the average (bounded) Flesch reading ease
    for the list of messages. 
    """    
  # Initialise total flesch reading ease variable
  total_flesch_reading_ease = 0
  
  # Sum all flesch reading eases for every message in messageList
  for message in messageList:
    total_flesch_reading_ease += calculateFleschReadingEase(message)

  # Return average flesch reading ease by dividing total flesch reading ease by length of messageList
  return total_flesch_reading_ease/len(messageList)
