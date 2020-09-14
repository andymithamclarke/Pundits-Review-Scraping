# =========================
# This file contains a function to clean the scraped text of irregularities
# =========================

# Irregularities found:

	# - '\n' can appear within the body of the text
	# - <p> elements can be too short and thus useless 


# Solutions implemented:

	# - Returning the <p> element only if it's str(length) is greater than 10 chars


# __Note__: 
# Expecting that there will be more solutions required as the volume of the corpus increases


def clean_text(full_text_list):
    
    return [item for item in full_text_list if len(item) > 10]