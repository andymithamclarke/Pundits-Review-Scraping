# =========================
# This file contains a function to return players from a phrase when they meet certain natural language characteristics
# =========================



# KEY: 
	# nsubj = main subject of a sentence
	# pobj = object of a preposition



# This function will use spaCy to return players that are either the main subject of a phrase or the object of a preposition
# First it will create a spaCy object from the phrase
# Then it will match words that meet the criteria: 
#			a) are either the "nsubj" or "pobj" of the phrase
#		    b) are a proper noun
#			c) have a length longer than 2 characters
# 			d) are listed as a player identifier
# Next it will re-match the player identifier with the original name of the player, given the parameter of "d" - a dictionary containing player names and identifiers for each team listed in the dataframe row
# It will return a list of the player names




# =============
#  IMPORTS 
# =============

import spacy



# =============
#  Save instance of spaCy model
# =============

nlp = spacy.load("en_core_web_sm")





# =============
#  The Function
# =============


def identify_nsubj_pobj(string, player_identifiers):
    
    # Create spacy object from string
    doc = nlp(string)
    
    # Create empty nsubj list
    nsubj_pobj = []
    
    # Iterate through doc object
    for i, tok in enumerate(doc):

        # ADDING NSUBJ
        # Check for NSubj only if tok is a proper noun and it's length is greater than 2
        if str(tok.dep_) == "nsubj" and str(tok.pos_) == "PROPN" and len(tok.text) > 2:
            # Apped subject if it matches with a player
            nsubj_pobj.append([player for player in list(player_identifiers.values()) if tok.text in player])

        # ADDING POBJ
        elif str(tok.dep_) == "pobj" and str(tok.pos_) == "PROPN" and len(tok.text) > 2:
            nsubj_pobj.append([player for player in list(player_identifiers.values()) if tok.text in player])
            
    # Empty Target List
    targets = []
    

    # Iterate through a flattened nsubj_pobj list
    for item in [y for x in nsubj_pobj for y in x]:

    	# Iterate through the players_identifiers dictionary passed as a parameter
        for key, value in player_identifiers.items():

        	# If the identifier is present in the players_identifiers dictionary - then add the official players name to the list of targets
            if str(item)[1:-1].replace("'", "") in value:
                targets.append(key)
            
    # return a flattened list - removing duplicate values        
    return list(dict.fromkeys(targets))




