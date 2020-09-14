# =========================
# This file contains functionality to calculate a players sentiment score 
# =========================


# There are two functions in this file :

# 1. calculate_sentiment_score ---> used to return a dictionary for each player containing the sentiment score of that player and more information 

	# Output ---->  dictionary ----> 'date | player | club | field_position | nationality | sentiment_score | sample_sentences | n_positive | n_negative | n_neutral | total_reviews'

# 2. sentiment_scores ---> used to build a dataframe containing rows for each unique player that has been identified 

	# Output ---->  pd.DataFrame ----> 'date | player | club | field_position | nationality | sentiment_score | sample_sentences | n_positive | n_negative | n_neutral | total_reviews'



#__Note:__
# 	- Sentiment scores are calculated as follows: Positive reviews as a percentage of total positive and negative reviews
#   - The method of calculation may need to be reviewed ... in order to consider number of total reviews (including neutral reviews)




# =============
#  IMPORTS 
# =============

import pandas as pd

# Local imports
import modules.players_dictionary as players_dictionary


# =============
#  Function 1. - calculate_sentiment_score
# =============

def calculate_sentiment_score(player, df):
    
    # Declare player dictionary - to be used as row in dataframe
    player_dictionary = {"sample_sentences": []}
    
    # Begin positive and negative scores at 0
    positive = 0
    negative = 0
    neutral = 0
    
    
    # Loop through dataframe and total up positive | negative scores
    for index, row in df.iterrows():
        
        # Add the date
        player_dictionary['date'] = row['date']
        
        # If the player is a target in the row
        if player in row['targets']:
            if row['sentiment'] == "POSITIVE":
                # Increment the positive counter
                positive += 1
                
                # Add the sentence to the players sample sentences
                player_dictionary['sample_sentences'].append({"sentiment": "POSITIVE", "url": row['url'], "media_source": row['media_source'], "original_sentence": row['original_sentence']})
                
            elif row['sentiment'] == "NEGATIVE":
                # Increment the negative counter
                negative += 1
                
                # Add the sentence to the players sample sentences
                player_dictionary['sample_sentences'].append({"sentiment": "NEGATIVE", "url": row['url'], "media_source": row['media_source'], "original_sentence": row['original_sentence']})
                
            elif row['sentiment'] == "NEUTRAL":
                # Increment the neutral counter
                neutral += 1
    
    # Calculate Player Score
    player_score = 0
    if (positive + negative) > 0:
        player_score += positive / (positive + negative)
    else: 
        player_score = positive
    
    # Make Dictionary Entries
    player_dictionary['player'] = player
    player_dictionary['n_positive'] = positive
    player_dictionary['n_negative'] = negative
    player_dictionary['n_neutral'] = neutral
    player_dictionary['total_reviews'] = positive + negative + neutral
    
    
    # If there are no positive or negative values attached to a player --> set their score to "N/A"
    if positive == 0 and negative == 0:
        player_dictionary['sentiment_score'] = "N/A"
    else:
        player_dictionary['sentiment_score'] = player_score
    
    # Find player in the players dictionary and add their information to the dictionary    
    for key, value in players_dictionary.players_dictionary.items():
        if player in list(value['squad_players'].keys()):
            player_dictionary['field_position'] = value['squad_players'][player]['position']
            player_dictionary['nationality'] = value['squad_players'][player]['nationality']
            player_dictionary['club'] = key
    
    return player_dictionary




# =============
#  Function 2. - sentiment_scores
# =============



def sentiment_scores(df):
    
    target_players = []
    
    for index, row in df.iterrows():
        for player in row['targets']:
            if player in target_players:
                pass
            else:
                target_players.append(player)
    
    list_of_player_dictionaries = []
    
    for player in target_players:
        list_of_player_dictionaries.append(calculate_sentiment_score(player, df))
        
    df_sentiment_scores = pd.DataFrame(list_of_player_dictionaries)
    
    df_sentiment_scores = df_sentiment_scores[["date", "player", "club", "field_position", "nationality", "sentiment_score", "sample_sentences", "n_positive", "n_negative", "n_neutral", "total_reviews"]]
    
    return df_sentiment_scores
