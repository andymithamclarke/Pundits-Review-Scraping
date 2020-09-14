# =========================
# This file contains a scrapy spider class used to return text from match reports
# =========================

# Steps:

	# 1. The spider will loop through the landing urls stored in the sources dictionary
	# 2. It will extract the article urls that match the specific landing_characteristics described in the sources dictionary
	# 3. It will then return a list of article dictionaries with the new article urls available from the corresponding source url - if that article url has not already been accessed
	# 4. Next each new article url is crawled
	# 5. The text is gathered from each article - according to specific article_characteristics described in the sources dictionary
	# 6. The text is then processed -- (cleaned, stopwords removed, teams identified, lemmatized and split into phrases)
	# 7. The output is a dataframe for each article with the structure outlined below
	# 8. Before returning, the dataframes are concatenated


# Output ---->  pd.DataFrame ----> 'date' | 'lemmatized_no_stopwords_phrase' | 'media_source' | 'original_sentence' | 'phrase' | 'teams' | 'time' | 'url'


# =============
#  IMPORTS 
# =============

import scrapy
from scrapy.crawler import CrawlerProcess
import logging
import pickle
import pandas as pd

# Local Imports
import modules.sources_dictionary as sources_dictionary
import modules.clean_text as clean_text
import modules.match_info as match_info
import modules.phrases as phrases



# ================
# Open list of previously accessed articles
# ================

# Specify Filename for previously accessed articles
filename_previously_accessed_articles = './pickles/previously_accessed_articles.sav'

# Read in previously_accessed_articles
previously_accessed_articles_infile = open(filename_previously_accessed_articles,'rb')

# Save instance of list 
previously_accessed_articles = pickle.load(previously_accessed_articles_infile)

# Close file
previously_accessed_articles_infile.close()


# ================
# Function to filter results from previously_accessed_articles
# ================

def filter(parsed_response):

	# Declare new list of unaccessed_urls
	unaccessed_urls = []

	# Iterate through the individual urls in parsed_response
	for item in parsed_response:

		# Check if url is in previously_accessed_articles 
		if item in previously_accessed_articles:
			continue
		# If item is not in previously_accessed_articles ----> append the item to previously_accessed_articles & add it to unaccessed_url list
		else:
			unaccessed_urls.append(item)
			previously_accessed_articles.append(item)


	return parsed_response


# ================
# The local variable to store the result of the process
# ================

df_list = []


# ================
# The Spider class which will return article links from each of the sources listed in the source dictionary
# ================

class ArticleSpider(scrapy.Spider):


	def __init__(self):
		self.name="ArticleSpider"


	# Specify filename for previously accessed articles
	filename_previously_accessed_articles = '../pickles/previously_accessed_articles.sav'


	# Function will be called automatically when spider crawls
	def start_requests(self):

		# Iterate through the sources_dictionary
		for key, value in sources_dictionary.sources_dictionary.items():

			# Iterate through the landing urls for each source
			for item in value['landing_urls']:

				# Make the request and pass the response to be parsed
				source_request = scrapy.Request(url=item, callback=self.parse_source)

				# Add the source name to the parse keywords parameter
				source_request.cb_kwargs['key'] = key

				# Process the response
				yield source_request


	# Callback function to return a dictionary of the new article urls for each source listed in the sources dictionary	
	def parse_source(self, response, key):

		parse_source_result = {

			"source": key,
			"article_urls": filter(list(dict.fromkeys(response.xpath(sources_dictionary.sources_dictionary[key]["landing_characteristics"]).extract()))),
			"characteristics": sources_dictionary.sources_dictionary[key]["article_characteristics"],
			"prefix": sources_dictionary.sources_dictionary[key]["article_url_prefix"],
			
		}

		# Iterate through the article_urls in parse_source_result
		for url in parse_source_result['article_urls']:

			# Prefix url - where required
			url_prefix = str(parse_source_result['prefix'] + url)

			# Make the request and pass the response to the callback function ----> self.parse_article
			article_request = scrapy.Request(url=url_prefix, callback=self.parse_article)

			# Add the source name to the parse keywords parameter
			article_request.cb_kwargs['media_source'] = parse_source_result['source']

			# Add the article characteristics to the parse keywords parameter
			article_request.cb_kwargs['characteristics'] = parse_source_result['characteristics']

			# Add the article url to the parse keywords parameter
			article_request.cb_kwargs['url'] = url_prefix

			# Process the response
			yield article_request

	

	# Callback function to parse the text in the article urls returned from parse_source
	# Function will return a list of dataframes after having processed and cleaned the text
	def parse_article(self, response, media_source, characteristics, url):

		# Clean the response object
		full_text = clean_text.clean_text(response.xpath(characteristics).extract())

		# Identify the teams in the match report
		teams = match_info.identify_teams(full_text)

		# Append the df_list with the result of the phrases.phraseify() function ---> Output is a dataframe for each of the articles in the same format as described in this documents header
		df_list.append(phrases.phraseify(full_text, teams, url, media_source))




# ================
# The function that will initialise the scraping process
# ================

def scrape():

	# !!! USER AGENT INFORMATION NEEDS TO BE CHANGED FOR OTHER USERS !!!

	# Initialise the Crawler Process with USER AGENT information
	process = CrawlerProcess({
    'USER_AGENT': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36; Andy Clarke/clarkeaj3@cardiff.ac.uk"
	})

	# Direct the process to the Article Spider
	process.crawl(ArticleSpider)

	# Start the spider
	process.start()

	# Dump the updated list into the same pickle file
	# *** LINES BELOW ARE COMMENTED FOR THE SAKE OF WORKING INSIDE OF A NOTEBOOK | UNCOMMENT FOR DEPLOYMENT ***

	# Open file
#-> previously_accessed_articles_outfile = open(filename,'wb')

	# Dump the updated list into the pickle
#-> pickle.dump(previously_accessed_articles, previously_accessed_articles_outfile)

	# Close the file
#-> previously_accessed_articles_outfile.close()


	# Return the concatenated dataframes - where teams have been identified!
	df = pd.concat(df_list)

	# Empty lists evaluate to false in boolean context
	# Reference this code = https://stackoverflow.com/questions/49700794/selecting-rows-of-pandas-dataframe-where-column-is-not-empty-list
	return df[df.teams.astype(bool)]

