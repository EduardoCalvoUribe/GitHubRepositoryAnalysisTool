# Copyright 2024 Radboud University, Modern Software Development Techniques

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This file contains the functions associated with computing the lexical density
"""

# Necessary imports for LexicalDensity.py
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

# A list of libraries which must be installed manually, as explained in project report.
# If libraries are downloaded, please comment them out.
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('tagsets')

# nltk.help.upenn_tagset() returns the list of all possible NLTK POS tags.

def singleMessageLexicalDensity(message):
  """
    Function which calculates the lexical density for a given message. This 
    metric is part of the general semantic score for commit and comment messages.

    Lexical density is a measure which can represent the relative meaningfulness of a text fragment. 
    The metric is dependent on the number of words in a commit message, and the number of nouns, adverbs, 
    verbs and adjectives (part of the set of linguistic lexical categories) in a commit message. 
    A high lexical density signifies that the commit message is informative/context-rich, whereas 
    a low lexical density might signify that the message lacks content. 

    Lexical density is computed as the number of lexical items (nouns, adjectives, verbs, adverbs)
    divided by the total number of words in a message. The resulting ratio is multiplied by 100
    to ensure that the value is bounded between 0 and 100. Words types are tagged with the use of
    NLTK POS tags. 
    
    NOTE: Words unknown to NLTK get tagged as a noun by default. 
    
    Parameters:
    message: The message for which the lexical density value is computed. Must be a string.

    Returns:
    float: A float between 0 and 100 representing the lexical density. If message is None (not defined) 
    or empty, the lexical density value is set to 0. 
  """
  # If message is None type (not defined) or empty, let lexical density equal 0  
  if message is None or message.strip() == "":
        return 0
  
  # Split message string into separate word tokens (i.e. substrings)
  tokens = word_tokenize(message)

  # Part of speech tagging using NLTK
  pos_tags = nltk.pos_tag(tokens)

  # Initialise list of POS tags which are lexical items (nouns, adjectives, verbs, adverbs)
  # Words unknown to NLTK get POS tag NN (noun) by default
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
    # Else return lexical density associated with message
    return (lexical_items_count/total_word_count)*100


# This function computes the average lexical density for a list of message strings.
# messageList must be a list of strings.
def averageMessageLexicalDensity(messageList):
  """
    Function which computes the average lexical density for a list of message strings.
    
    Parameters:
    messageList: The list of messages for which the average lexical density
    is computed. Must be a list of strings. 

    Returns:
    float: A float between 0 and 100 representing the average lexical density
    for the list of messages. 
    """   
  # Initialise total lexical density variable
  total_lexical_density = 0
  
  # Sum all lexical densities for every message in messageList
  for message in messageList:
    total_lexical_density += singleMessageLexicalDensity(message)

  # Return average lexical density by dividing total lexical density by length of messageList
  return total_lexical_density/len(messageList)

  
