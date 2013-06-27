
from actions.screenshot import Screenshot
from actions.youtube import Youtube
from actions.wolfram import Wolfram
from actions.music import Music
from actions.news import News
from actions.webpage import Webpage

import webbrowser
import os


class VoiceCommand:
	"""
	distributes jobs to an appropriate action in the actions folder. 
	"""

	def __init__(self, speaker):
		self.speaker = speaker
		self.controller = webbrowser.get()

		# initialize action class instances
		self.Youtube = Youtube(self.speaker)
		self.Wolfram = Wolfram(self.speaker, os.environ.get('WOLFRAM_API_KEY'))
		self.Music = Music(self.speaker)
		self.Screenshot = Screenshot(self.speaker)
		self.News = News(self.speaker)
		self.Webpage = Webpage(self.speaker)

	def accidental_recording(self):
		print "---Accidental recording---"
		print "Saying: Oops, sorry."
		self.speaker.play_wav("./wav/sorry.wav")

	def open_webpage(self, job):
		self.Webpage.process(job, self.controller)

	def google(self, job):
		self.speaker.say("searching...")
		google_url = "http://www.google.com/search?q="
		phrase = job.query
		url = google_url + phrase.replace(" ", "+")
		self.controller.open(url)

	def search_youtube(self, job):
		self.Youtube.search(job, self.controller)

	def play_youtube(self, job):
		self.Youtube.process(job, self.controller)

	def take_screenshot(self):
		self.Screenshot.take()

	def ai_respond(self, job, AI):
		if job.query != "":
			response = AI.respond(job.query)
		else:
			response = AI.respond(job.recorded())
		self.speaker.say(response)

	def get_news(self, job):
		self.News.process(job, self.controller)

	def change_news_source(self, job):
		self.News.set_news_url()

	def ask_wolfram(self, job, AI):
		if not self.Wolfram.process(job, self.controller):
			self.ai_respond(job, AI)
			job.is_processed = True

	def play_music(self, job):
		self.Music.process(job, self.controller)