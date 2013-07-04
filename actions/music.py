

class Music():
	"""
	Process requests to play music.
	
	"""
	def __init__(self, speaker, actions_helper):
		self.speaker = speaker
		self.helper = actions_helper

	def process(self, job, controller):
		"""Process play radio job request."""
		# TODO make check of whether last.fm is not already open.
		# Last.fm radio glitches out when two or more of them 
		# run at the same time.
		self.speaker.say("Starting radio.")
		phrase = job.query
		phrase = self.replace_spaces(phrase)
		music_url = "http://www.last.fm/listen/artist/" + \
					phrase + "/similarartists"
		if self.helper.test_url(music_url) != "":
			controller.open(music_url)
		else:
			self.speaker.say("Oops, page does not exist.")

	def replace_spaces(self, phrase):
		"""Replace spaces in string with %2B."""
		space = phrase.find(' ')
		while space != -1:
			phrase = phrase[:space] + "%2B" + phrase[space + 1:]
			space = phrase.find(' ')
		return phrase.lower()

	