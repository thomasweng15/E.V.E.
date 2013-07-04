from actions.actions_helper import ActionsHelper

class Search():
	"""
	Process web searches.
	
	"""
	def __init__(self, speaker):
		self.speaker = speaker
		# self.get_search_url()

	'''
	def get_search_url(self):
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
	'''


	def process(self, job, controller):
		"""Process web search job request."""
		self.speaker.say("searching...")
		search_url = "http://www.google.com/search?q="
		phrase = job.query
		url = search_url + phrase.replace(" ", "+")
		controller.open(url)