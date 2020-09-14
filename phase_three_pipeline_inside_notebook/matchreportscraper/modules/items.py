# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PhraseItem(scrapy.Item):
	date = scrapy.Field()
	lemmatized_no_stopwords_phrase = scrapy.Field()
	media_source = scrapy.Field()
	original_sentence = scrapy.Field()
	phrase = scrapy.Field()
	teams = scrapy.Field()
	time = scrapy.Field()
	url = scrapy.Field()

