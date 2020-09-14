# =========================
# This file contains a function to loop through the dataframe and return target players
# =========================



# Function will loop through the rows in the dataframe
# It will then loop through the players in the teams listed 
# Using the function 'identify_nsubj_pobj' it will identify players listed in the sentence from their player identifiers listed in 'players dictionary'
# It will add a list of the target players to the dataframe's corresponding row
# Finally it will return a dataframe in which rows without target players have been removed


#__Note__: 
# Problems still occur when players have the same surname


# =============
#  IMPORTS 
# =============


# Local imports
import modules.players_dictionary as players_dictionary
import modules.identify_nsubj_pobj as identify_nsubj_pobj



# =============
#  The Function
# =============

def target_identifier(df):
    
    # Define an empty players list
    player_list = []
    

    # Iterate through the dataframe passed as a parameter
    for index, row in df.iterrows():
        
        # Create an empty dictionary to store players as keys and player identifiers as values
        d = {}

        # Iterate through the teams listed in each row
        for team in row['teams']:

        	# Save the dictionary of squad players from the 'players_dictionary' module that match each team listed in the row
            squad_players = players_dictionary.players_dictionary[team]['squad_players']
            # Add the teams to the dictionary
            d[team] = players_dictionary.players_dictionary[team]['name_variations']
            
            # Make a dictionary holding the players names and player identifiers = d
            for player_key, player_value in squad_players.items():
                d[player_key] = player_value['identifiers']

        # Use the identify_nsubj_pobj function to return a list of the target players in the phrase      
        if identify_nsubj_pobj.identify_nsubj_pobj(row['phrase'], d):
        	# If there is a match --->  Append the player targets to the player_list
            player_list.append(identify_nsubj_pobj.identify_nsubj_pobj(row['phrase'], d))
        else: 
        	# If there is no match ----> Append and empty string
            player_list.append("")
    
    # Add the players list to a new column in the dataframe
    df['targets'] = player_list
    

    # Return the dataframe whilst removing rows where a target was not found
    return df[df['targets'] != ""]