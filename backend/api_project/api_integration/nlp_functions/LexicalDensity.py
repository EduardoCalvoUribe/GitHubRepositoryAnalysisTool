import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

# Necessary dependencies for proper word_tokenize and pos_tag functionality.
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# This function computes the lexical density for a message string using NLTK
# POS (part of speech) tagging.
def singleMessageLexicalDensity(message):
  # If message is None type (not defined) or empty, let lexical density equal 0  
  if message is None or message.strip() == "":
        return 0
  
  # Split message string into separate word tokens (i.e. substrings)
  tokens = word_tokenize(message)

  # Part of speech tagging
  pos_tags = nltk.pos_tag(tokens)

  # List of POS tags which are lexical items (nouns, adjectives, verbs, adverbs)
  # Words unknown to nltk get POS tag NN (noun) by default
  lexical_items = ['NN', 'NNS', 'NNP', 'NNPS',  # Nouns
                         'JJ', 'JJR', 'JJS',         # Adjectives
                         'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ',  # Verbs
                         'RB', 'RBR', 'RBS', 'WRB']         # Adverbs
                  
  # Initialise lexical items count                 
  lexical_items_count = 0

  # Total word count
  total_word_count = len(tokens)

  # Loop over every word in pos_tags. If tag in lexical_items increase count by 1.
  for word, tag in pos_tags:
    if tag in lexical_items:
      lexical_items_count += 1
  

  # If message string is empty
  if total_word_count == 0:
    return 0 
  else:
    return (lexical_items_count/total_word_count)*100


# This function computes the average lexical density for a list of message strings.
# messageList must be a list of strings.
def averageMessageLexicalDensity(messageList):
  # Initialise total lexical density variable
  total_lexical_density = 0
  
  # Sum all lexical densities for every message in messageList
  for message in messageList:
    total_lexical_density += singleMessageLexicalDensity(message)

  # Return average lexical density by dividing total lexical density by length of messageList
  return total_lexical_density/len(messageList)


# Code for getting list of possible nltk POS tags
# nltk.download('tagsets')
# nltk.help.upenn_tagset()
  
