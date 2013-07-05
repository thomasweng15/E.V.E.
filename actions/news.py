import sys


class News():
	"""
	Process jobs requesting the news.
	
	"""
	def __init__(self, speaker, actions_helper):
		self.speaker = speaker
		self.helper = actions_helper
		self.news_url = self.helper.get_value_from_datafile("news_url")

	def process(self, job, controller):
		"""Process News job request."""
		self.speaker.say("getting the news.")
		controller.open(self.news_url)

	

	