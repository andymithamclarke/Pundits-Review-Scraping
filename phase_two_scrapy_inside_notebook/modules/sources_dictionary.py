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
	}
}
