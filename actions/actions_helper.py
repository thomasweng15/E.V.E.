import urllib2

class ActionsHelper():
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