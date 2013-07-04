
from actions.screenshot import Screenshot
from actions.youtube import Youtube
from actions.wolfram import Wolfram
from actions.music import Music
from actions.news import News
from actions.webpage import Webpage
from actions.chatbot import Chatbot

import webbrowser
import os


class VoiceCommand:
	"""
	Distribute jobs to the appropriate action.

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
		self.Chatbot = Chatbot(self.speaker)

	def accidental_recording(self):
		"""Started recording by accident, just post message."""
		print "---Accidental recording---"
		print "Saying: Oops, sorry."
		self.speaker.play_wav("./wav/sorry.wav")

	def open_webpage(self, job):
		"""Send to open webpage action."""
		self.Webpage.process(job, self.controller)

	def search(self, job):
		"""Send to web search action."""
		self.Search.process(job, self.controller)

	def search_youtube(self, job):
		"""Send to search youtube action."""
		self.Youtube.search(job, self.controller)

	def play_youtube(self, job):
		"""Send to play first youtube video from search action."""
		self.Youtube.process(job, self.controller)

	def take_screenshot(self):
		"""Send to take screenshot action."""
		self.Screenshot.take()

	def chatbot_respond(self, job):
		"""Send to chatbot to respond action."""
		self.Chatbot.process(job)

	def get_news(self, job):
		"""Send to open news action."""
		self.News.process(job, self.controller)

	def change_news_source(self, job):
		"""Send to change news url action."""
		self.News.set_news_url()

	def ask_wolfram(self, job):
		"""
		Send to WolframAlpha for a response. 
		If no response is found, send to chatbot.

		"""
		if not self.Wolfram.process(job, self.controller):
			self.chatbot_respond(job)

	def play_music(self, job):
		"""Send to play radio action."""
		self.Music.process(job, self.controller)