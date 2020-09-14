# =========================
# This file contains a function to predict the sentiment of phrases within a football match report
# =========================


# The function uses a trained classifier and vectorizer which have been pickled and saved in the pickles directory of this project

# It will loop through the dataframe passed as a parameter and extract a list of lemmatized no stopwords phrases
# It will then make a prediction based on a vectorized form of the lemmatized no stopwords phrases
# It will return a list of predictions for each phrase as either 'POSITIVE', "NEUTRAL" or "NEGATIVE"


# =============
#  IMPORTS 
# =============

import pickle

# Pickles

# Import the vectorizer
cv_1_1_infile_vect = open("./pickles/cv_1_1.sav",'rb')

# Save instance of vectorizer
vectorizer = pickle.load(cv_1_1_infile_vect)

# Close file
cv_1_1_infile_vect.close()

# Read in model
logreg_cv_1_1_infile_model = open("./pickles/logreg_cv_1_1.sav",'rb')

# Save instance of model
model = pickle.load(logreg_cv_1_1_infile_model)

# Close file
logreg_cv_1_1_infile_model.close()



# =============
# The Function 
# =============


def predict(df):
    
    # Sentence List
    sentences = []
    
    # Iterate through df and append sentences to sentences list
    for index, row in df.iterrows():
        
        # Append Sentences list with sentences
        sentences.append(row['lemmatized_no_stopwords_phrase'])
    
    # Iterate through sentences list and make predictions
    predictions = model.predict(vectorizer.transform(sentences))
        
    # Return List of Predictions
    return predictions



