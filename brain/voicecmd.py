
from actions.screenshot import Screenshot
from actions.youtube import Youtube
from actions.wolfram import Wolfram

import webbrowser
import urllib2
import praw
import os


class VoiceCommand:
	def __init__(self, speaker):
		self.speaker = speaker
		self.controller = webbrowser.get()

	def accidental_recording(self):
		print "---Accidental recording---"
		print "Saying: Oops, sorry."
		self.speaker.play_wav("./wav/sorry.wav")

	def open_webpage(self, job):
		phrase = job.recorded()[job.recorded().find(' ') + 1:]
		url = self._make_url(phrase)
		if url != "":
			self.speaker.say("opening " + url[12:])
			self.controller.open(url)
		else:
			self.speaker.say("sorry, I didn't find the web page.")

	def _make_url(self, phrase):
		# remove spaces in the phrase
		phrase = self._remove_spaces(phrase)

		# if phrase does not end with .com or other suffix append .com
		if phrase.find('.com') == -1 \
		and phrase.find('.edu') == -1 \
		and phrase.find('.org') == -1:
			phrase = phrase + ".com"

		# test website existence, return "" if website doesn't exist
		return self._test_url(phrase)

	def _remove_spaces(self, phrase):
		space = phrase.find(' ')
		while space != -1:
			phrase = phrase[:space] + phrase[space + 1:]
			space = phrase.find(' ')
		return "https://www." + phrase.lower()

	def _test_url(self, phrase):
		try: 
			phrase = phrase.lower()
			code = urllib2.urlopen(phrase).code
			if (code / 100 >= 4):
				return ""
			else: 
				return phrase
		except urllib2.URLError as err: pass
		return ""

	def google(self, job):
		self.speaker.say("searching...")
		google_url = "http://www.google.com/search?q="
		phrase = job.recorded()[job.recorded().find(' ') + 1:]
		url = google_url + phrase.replace(" ", "+")
		self.controller.open(url)

	def youtube(self, job, option):
		if option == "search":
			self.speaker.say("Pulling up youtube results.")
			y_url = "http://www.youtube.com/results?search_query="
			phrase = job.recorded()[job.recorded().find(' ') + 1:]
			phrase = phrase[job.recorded().find(' ') + 1:]
			url = y_url + phrase.replace(" ", "+")
			self.controller.open(url)
		else:
			self.speaker.say("Playing video.")
			Youtube(self.speaker).process(job, self.controller)

	def screenshot(self):
		Screenshot(self.speaker).take()

	def ai_respond(self, job, AI, memory):
		response = AI.respond(job.recorded()[8:], memory)
		self.speaker.say(response)

	def get_news(self):
		self.speaker.say("getting the world news.")
		r = praw.Reddit(user_agent='evebot v1.0 by /u/tw334')
		submissions = r.get_subreddit('worldnews').get_new(limit=10)
		# TODO make titles spoken
		for submission in submissions:
			print ">>> " + submission.title

	def wolfram(self, job):
		Wolfram(self.speaker, os.environ.get('WOLFRAM_API_KEY')).process(job, self.controller)

	