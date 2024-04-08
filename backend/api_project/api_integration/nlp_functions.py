# from django.http import HttpResponse

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
def calculate_flesch_reading_ease(message):
    # Word count equals message string length
    wordCount = len(message)
    # Count sentences using nltk sent_tokenize
    sentenceCount = len(sent_tokenize(message))
    # Initialise syllable count for message using syllable_count function.
    syllableCount = 0

    # Count total syllable count
    for word in message:
        syllableCount += syllable_count(word)
    
    return str(206.835 - (1.015 * (wordCount/sentenceCount)) - (84.6 * (syllableCount/wordCount)))

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