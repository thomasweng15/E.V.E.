import urllib2

DATAFILE = "./data/user_config.txt"

class ActionsHelper():
	"""
	contains helper functions for actions.
	"""

	def test_url(self, phrase):
		try: 
			phrase = phrase.lower()
			code = urllib2.urlopen(phrase).code
			if (code / 100 >= 4):
				return ""
			else: 
				return phrase
		except urllib2.URLError as err: pass
		return ""

	def get_url_from_datafile(self, which_url):
		try:
			f = open(DATAFILE, 'r')
		except IOError:
			self.speaker.say("Error, datafile cannot be found.")
			sys.exit(1)

		found_search_url = False
		for line in f:
			if line.find("search_url::") != -1:
				self.search_url = line[10:]
				found_search_url = True
				break

		if found_news_url != True:
			self.speaker.say("Oops, datafile does not contain news URL item.")
		f.close()