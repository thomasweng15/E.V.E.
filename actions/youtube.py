from urllib2 import urlopen
import json


class Youtube:
	"""
	processes jobs requesting to interact with YouTube.
	"""

	def __init__(self, speaker):
		self.speaker = speaker

	def process(self, job, controller):
		self.speaker.say("Playing video.")

		if job.get_is_processed():
			return False
			
		result = self.get_first_video(job.query, controller)
		job.is_processed = True

	# get the URL of the first video and open in firefox
	def get_first_video(self, phrase, controller):
		y_url = "http://gdata.youtube.com/feeds/api/videos?max-results=1&alt=json&orderby=relevance&q="
		url = y_url + phrase.replace(" ", "+")
		inp = urlopen(url)
		resp = json.load(inp)
		inp.close()

		first = resp['feed']['entry'][0]
		url = first['link'][0]['href']
		controller.open(url)

	def search(self, job, controller):
		self.speaker.say("Pulling up youtube results.")
		y_url = "http://www.youtube.com/results?search_query="
		phrase = job.query
		url = y_url + phrase.replace(" ", "+")
		controller.open(url)
	


