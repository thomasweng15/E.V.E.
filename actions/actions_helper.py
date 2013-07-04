import urllib2

DATAFILE = "./data/user_config.txt"

class ActionsHelper():
	"""
	Hold helper functions for actions.
	
	"""
	def __init__(self, speaker):
		self.speaker = speaker

	def test_url(self, phrase):
		"""Test existence of domain at url."""
		try: 
			phrase = phrase.lower()
			code = urllib2.urlopen(phrase).code
			if (code / 100 >= 4):
				return ""
			else: 
				return phrase
		except urllib2.URLError as err: pass
		return ""

	def get_value_from_datafile(self, key):
		"""Find key and return value from datafile."""
		try:
			f = open(DATAFILE, 'r')
		except IOError:
			self.speaker.say("Error, datafile cannot be found.")
			sys.exit(1)

		for line in f:
			if line.find(key + "::") != -1:
				f.close()
				return line[len(key + "::"):].rstrip('\n')

		self.speaker.say("Oops, datafile does not contain the needed info.")
		f.close()
		return None