

class Search():
	"""
	Process web searches.
	
	"""
	def __init__(self, speaker, actions_helper):
		self.speaker = speaker
		self.helper = actions_helper
		self.search_url = self.helper.get_value_from_datafile("search_url")

	def process(self, job, controller):
		"""Process web search job request."""
		self.speaker.say("Pulling up search results.")
		phrase = job.query
		url = self.search_url + phrase.replace(" ", "+")
		controller.open(url)