# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pandas as pd
import modules.target_identifier as target_identifier
import modules.players_dictionary as original_players_dictionary
import modules.predict as predict
import csv 

# ================
# PIPELINE 1 ---> Identify Sentiment in Phrases
# ================


class IdentifySentimentPipeline:

	def process_item(self, item, spider):

		sentiment_dictionary = predict.predict(item)
		return sentiment_dictionary



# ================
# PIPELINE 2 ---> Calculate Sentiment Scores
# ================


class CalculateScorePipeline:

	players_dictionary = {}

	def close_spider(self, spider):

		list_of_score_dictionaries = []
		
		for key, value in self.players_dictionary.items():
			score_dictionary = {
				"date": value['date'],
				"player": value['player'],
				"sample_sentences": value['sample_sentences'],
				"sentiment_score": "",
				"nationality": value['nationality'],
				"club": value['club'],
				"field_position": value['field_position'],
				"n_positive": value['n_positive'],
				"n_negative": value['n_negative'],
				"n_neutral": value['n_neutral'],
				"total_reviews": value['total_reviews']
			}

			if value['n_positive'] == 0 and value['n_negative'] == 0:
				score_dictionary['sentiment_score'] = "N/A"
			else:
				score_dictionary['sentiment_score'] = (value['n_positive'] / (value['n_positive'] + value['n_negative']))


			list_of_score_dictionaries.append(score_dictionary)

		df = pd.DataFrame(list_of_score_dictionaries)
		df.to_csv('test.csv', index=False)




	def process_item(self, item, spider):

		for player in item['targets']:

			if player in list(self.players_dictionary.keys()):
				if item['sentiment'] == "NEGATIVE":
					self.players_dictionary[player]['n_negative'] += 1
					self.players_dictionary[player]['total_reviews'] += 1
					self.players_dictionary[player]['sample_sentences'].append({"sentiment": "NEGATIVE", "url": item['url'], "media_source": item['media_source'], "original_sentence": item['original_sentence']})
				elif item['sentiment'] == "POSITIVE":
					self.players_dictionary[player]['n_positive'] += 1
					self.players_dictionary[player]['total_reviews'] += 1
					self.players_dictionary[player]['sample_sentences'].append({"sentiment": "POSITIVE", "url": item['url'], "media_source": item['media_source'], "original_sentence": item['original_sentence']})
				else:
					self.players_dictionary[player]['n_neutral'] += 1
					self.players_dictionary[player]['total_reviews'] += 1
			else:
				self.players_dictionary[player] = {
					"date": item['date'],
					"player": player,
					"sample_sentences": [],
					"nationality": "",
					"club": "",
					"field_position": "",
					"n_positive": 0,
					"n_negative": 0,
					"n_neutral": 0,
					"total_reviews": 0
				}

				# Adding Player Info
				for key, value in original_players_dictionary.premier_league_players_dictionary.items():
					if player in list(value['squad_players'].keys()):
						self.players_dictionary[player]['field_position'] = value['squad_players'][player]['position']
						self.players_dictionary[player]['nationality'] = value['squad_players'][player]['nationality']
						self.players_dictionary[player]['club'] = key

				# Adding Sentiment Scores
				if item['sentiment'] == "NEGATIVE":
					self.players_dictionary[player]['n_negative'] += 1
					self.players_dictionary[player]['total_reviews'] += 1
					self.players_dictionary[player]['sample_sentences'].append({"sentiment": "NEGATIVE", "url": item['url'], "media_source": item['media_source'], "original_sentence": item['original_sentence']})
				elif item['sentiment'] == "POSITIVE":
					self.players_dictionary[player]['n_positive'] += 1
					self.players_dictionary[player]['total_reviews'] += 1
					self.players_dictionary[player]['sample_sentences'].append({"sentiment": "POSITIVE", "url": item['url'], "media_source": item['media_source'], "original_sentence": item['original_sentence']})
				else:
					self.players_dictionary[player]['n_neutral'] += 1
					self.players_dictionary[player]['total_reviews'] += 1

		


		#return self.players_dictionary