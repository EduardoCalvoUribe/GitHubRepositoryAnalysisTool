# Copyright 2024 Radboud University, Modern Software Development Techniques

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from datetime import datetime, timedelta
from models import User, Repository
import numpy as np

# Logistic conversion function
def logistic_conversion(x, k=10):
    return 100 / (1 + np.exp(-k * (x - 1)))

def week_range():
    return None


# Function to calculate decay for each week
def calculate_decay_scores(weeks=8, decay_rate=float, k=int):
    scores = []
    total_weight = 0
    
    for week in range(weeks):
        start_date = datetime.today() - timedelta(weeks=week+1)
        end_date = datetime.today() - timedelta(weeks=week)
        
        # Filter data for the specific week
        #user_week_ccp = sum(ccp for date, ccp in user_ccp if start_date <= date < end_date)
        #avg_week_ccp = sum(ccp for date, ccp in avg_ccp if start_date <= date < end_date) / len(avg_ccp) if avg_ccp else 1
        
        if avg_week_ccp == 0:  # Avoid division by zero
            avg_week_ccp = 1
        
        # Calculate the activity ratio and apply logistic conversion
        #ratio = user_week_ccp / avg_week_ccp
        #score = logistic_conversion(ratio, k)
        
        # Apply decay to the score
        decay_weight = decay_rate ** week
        #decayed_score = score * decay_weight
        #scores.append(decayed_score)
        total_weight += decay_weight
    
    # Sum the decayed scores
    total_score = sum(scores)
    
    # Average the score based on decay weights
    average_score = total_score / total_weight if total_weight > 0 else 0
    
    return average_score

# Function to calculate the final engagement score
def calculate_engagement_score(decay_rate=0.85, k=10):
    # Calculate the decayed logistic conversion score
    decayed_logistic_score = calculate_decay_scores(decay_rate=decay_rate, k=k)
    
    # Calculate the average semantic score
    #average_semantic_score = sum(comment_scores) / len(comment_scores) if comment_scores else 0
    average_semantic_score = min(max(average_semantic_score, 0), 100)  # Ensure the score is between 0 and 100
    
    # Final score formula
    final_score = (decayed_logistic_score * 0.5) + (average_semantic_score * 0.5)
    
    # Ensure the final score is between 0 and 100
    final_score = min(max(final_score, 0), 100)
    
    return final_score

# Calculate the amount of a specic user commits, comments and pull requests
def calculateCcpUser(user):
    return len(user.commits.values()) + len(user.comments.values()) + len(user.pullrequests.values())
    
# Calculate the average user of a repository commits, comments and pull requests
def calculateCcpAvg(contributors):
    total = 0
    for user in contributors:
        total += len(user.commits.values()) + len(user.comments.values()) + len(user.pullrequests.values())
    return total / len(contributors)

# Calculate the final engagement score
engagement_score = calculate_engagement_score(decay_rate=0.85, k=10)




