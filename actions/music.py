from actions.actions_helper import ActionsHelper


class Music():
	"""
	processes requests to play music.
	"""

	def __init__(self, speaker):
		self.speaker = speaker

	def process(self, job, controller):
		# TODO make check of whether last.fm is not already open.
		# Last.fm radio glitches out when two or more of them 
		# run at the same time.
		self.speaker.say("Starting radio.")
		phrase = job.recorded()[job.recorded().find(' ') + 1:]
		phrase = self._replace_spaces(phrase)
		music_url = "http://www.last.fm/listen/artist/" + \
					phrase + "/similarartists"
		if ActionsHelper().test_url(music_url) != "":
			controller.open(music_url)
		else:
			self.speaker.say("Oops, page does not exist.")

	def _replace_spaces(self, phrase):
		space = phrase.find(' ')
		while space != -1:
			phrase = phrase[:space] + "%2B" + phrase[space + 1:]
			space = phrase.find(' ')
		return phrase.lower()

	