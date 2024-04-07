import nltk

# download cmudict
nltk.download('cmudict')
#import cmudict (pronounciation dictionary) for annotated syllables
from nltk.corpus import cmudict
# read in cmudict as dictionary
d = cmudict.dict()


#Function which calculates the Flesch reading ease metric for a given message.
def calculate_flesch_reading_ease(message):
    print("test")

# Function which uses cmudict to return number of syllables, if word not in cmudict then number of syllables is counted manually. 
# Courtesy of https://datascience.stackexchange.com/questions/23376/how-to-get-the-number-of-syllables-in-a-word
def syllable_count(word):
    if word.lower() in d:
        return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]
    else:
        # if word not found in cmudict
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