# =========================
# This file contains a dictionary with all the landing urls for sources used in my system
# -----
# - These urls will be visited and article urls scraped from them
# =========================

# Note: This file will be updated frequently with more source urls

# 		- Need to edit BBC Fixtures so that url is generated from current year and month


sources_dictionary = {


	"The Mirror - Match Reports": {
		"landing_urls": ["https://www.mirror.co.uk/sport/football/match-reports/", "https://www.mirror.co.uk/sport/football/match-reports/?pageNumber=2", "https://www.mirror.co.uk/sport/football/match-reports/?pageNumber=3"],
		"landing_characteristics": '//a[contains(@href, "match-report")]/@href',
		"article_characteristics": "//p/text()",
		"article_url_prefix": ""
	},
	"The Guardian - Match Reports": {
		"landing_urls": ["https://www.theguardian.com/football/football+tone/matchreports", "https://www.theguardian.com/football/football+tone/matchreports?page=2", "https://www.theguardian.com/football/football+tone/matchreports?page=3"],
		"landing_characteristics": '//a[contains(@data-link-name, "article")]/@href',
		"article_characteristics": "//p/text()",
		"article_url_prefix": ""
	},
	"The Guardian - Minute by Minutes": {
		"landing_urls": ["https://www.theguardian.com/football/football+tone/minutebyminute", "https://www.theguardian.com/football/football+tone/minutebyminute?page=2", "https://www.theguardian.com/football/football+tone/minutebyminute?page=3"],
		"landing_characteristics": '//a[contains(@data-link-name, "article")]/@href',
		"article_characteristics": "//p/text()",
		"article_url_prefix": ""
	},
	"Sky Sports - Premier League Results": {
		"landing_urls": ["https://www.skysports.com/premier-league-results"],
		"landing_characteristics": '//a[contains(@class, "matches__link")]/@href',
		"article_characteristics": "//p/text()",
		"article_url_prefix": ""
	},
	"EPL Analysis - Match Analysis": {
		"landing_urls": ["https://eplanalysis.com/category/analysis/match-analysis", "https://eplanalysis.com/category/analysis/match-analysis/page/2", "https://eplanalysis.com/category/analysis/match-analysis/page/3"],
		"landing_characteristics": '//div[contains(@class, "main-content")]//a[contains(@rel, "bookmark")]/@href',
		"article_characteristics": "//p/text()",
		"article_url_prefix": ""
	},
	"EPL Analysis - Player Analysis": {
		"landing_urls": ["https://eplanalysis.com/category/analysis/player-analysis", "https://eplanalysis.com/category/analysis/player-analysis/page/2", "https://eplanalysis.com/category/analysis/player-analysis/page/3"],
		"landing_characteristics": '//div[contains(@class, "main-content")]//a[contains(@rel, "bookmark")]/@href',
		"article_characteristics": "//p/text()",
		"article_url_prefix": ""
	},
	"Coaches Voice - The Game": {
		"landing_urls": ["https://www.coachesvoice.com/category/the-game/", "https://www.coachesvoice.com/category/the-game/page/2/", "https://www.coachesvoice.com/category/the-game/page/3/", "https://www.coachesvoice.com/category/the-game/page/4/"],
		"landing_characteristics": '//div[contains(@class, "top")]//a/@href',
		"article_characteristics": "//p/text()",
		"article_url_prefix": ""
	},
	"BBC Sport - Premier League Scores and Fixtures": {
		"landing_urls": ["https://www.bbc.co.uk/sport/football/premier-league/scores-fixtures/2020-03"],
		"landing_characteristics": '//a[contains(@class, "sp-c-fixture__block-link")]/@href',
		"article_characteristics": "//p/text()",
		"article_url_prefix": "https://www.bbc.co.uk/"
	}
}

