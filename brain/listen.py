#!/usr/bin/python
# -*- coding: utf-8 -*-

from inputs.microphone import Microphone
from ex.exception import NotUnderstoodException
from actions.screenshot import Screenshot
from actions.wolfram import Wolfram
from actions.youtube import Youtube
# from actions.gmusic import GoogleMusic

import tts
import stt
import webbrowser
import os
import sys
import praw
import urllib2


class Job:
	def __init__(self, raw):
		self.raw_text = raw
		self.is_processed = False

	def get_is_processed(self):
		return self.is_processed

	def raw(self):
		return self.raw_text


class Listen():
	def __init__(self, AI):
		print "Saying: Yes?"
		self.speaker = tts.Google()
		self.speaker.play_wav("./wav/yes.wav")
		self.AI = AI
		
		self.listen()

	def listen(self):
		try:
			audioInput = Microphone()
			audioInput.listen()
	 
			speech_to_text = stt.Google(audioInput)
			recorded_text = speech_to_text.get_text()
			job = Job(recorded_text)

			controller = webbrowser.get() # init controller for browser

			# parse first and second words in command
			first_word = (recorded_text.split(' ')[0]).lower() 
			if recorded_text.find(' ') >= 1:
				second_word = (recorded_text.split(' ')[1]).lower()
			else:
				second_word = ""

			# execute commands based on first word in query
			if first_word == "stop" or first_word == "no" \
					or recorded_text.find('no stop') != -1:
				print "---Accidental recording---"
				print "Saying: Oops, sorry."
				self.speaker.play_wav("./wav/sorry.wav")

			elif first_word == "open":
				if second_word != "": # open webpage
					phrase = recorded_text[recorded_text.find(' ') + 1:]
					url = self.make_url(phrase)

					if url != "": 
						self.speaker.say("opening " + url[12:])
						controller.open(url)
					
					else: 
						self.speaker.say("sorry, I didn't find the web page.")

				else:
					self.speaker.say("no webpage specified.")

			elif first_word == "google" or first_word == "search": 
				if second_word != "": # pull up query results
					self.speaker.say("searching...")
					google_url = "http://www.google.com/search?q="
					phrase = recorded_text[recorded_text.find(' ') + 1:]
					url = google_url + phrase.replace(" ", "+")
					controller.open(url)

				else: # no query provided, just open google
					self.speaker.say("opening google.com.")
					url = "http://www.google.com"
					controller.open(url)

			elif recorded_text.find('news') != -1:
				self.speaker.say("getting the world news.")

				r = praw.Reddit(user_agent='evebot v1.0 by /u/tw334')
				submissions = r.get_subreddit('worldnews').get_new(limit=10)
				# TODO make titles spoken
				for submission in submissions:
					print ">>> " + submission.title

			elif first_word == "youtube":
				if second_word != "": 
					if second_word == "search": # return youtube search results
						self.speaker.say("Pulling up youtube results.")
						y_url = "http://www.youtube.com/results?search_query="
						phrase = recorded_text[recorded_text.find(' ') + 1:]
						phrase = phrase[recorded_text.find(' ') + 1:]
						url = y_url + phrase.replace(" ", "+")
						controller.open(url)

					else: # open first youtube video associated with query
						self.speaker.say("Playing video.")
						Youtube(self.speaker).process(job)

				else: 
					self.speaker.say("Opening youtube.com.")
					url = "http://www.youtube.com"
					controller.open(url)

			elif first_word == "play" or first_word == "grooveshark":
				self.speaker.say("opening Grooveshark.")
				
				if second_word != "": # pull up Grooveshark search results
					# TODO auto play first music item from search results
					grooveshark_url = "http://grooveshark.com/#!/search?q="
					phrase = recorded_text[recorded_text.find(' ') + 1:]
					url = grooveshark_url + phrase.replace(" ", "+")
					controller.open(url)

				else:
					url = "http://grooveshark.com"
					controller.open(url)

			elif recorded_text.lower().find('screenshot') != -1:
				Screenshot(self.speaker).take()

			elif first_word == "computer": # AI responds
				response = self.AI.respond(recorded_text[8:], "Thomas")
				self.speaker.say(response) 

			else: 
				Wolfram(self.speaker, 
						os.environ.get('WOLFRAM_API_KEY')).process(job)

			if not job.get_is_processed:
				self.speaker.say("Sorry, I didn't find any results.")

		except NotUnderstoodException:
			print "Sorry, I didn't understand what you said."
			self.speaker.play_wav("./wav/didntget.wav")

	def make_url(self, phrase):
		# remove spaces in phrase
		space = phrase.find(' ')
		while space != -1:
			phrase = phrase[:space] + phrase[space + 1:]
			space = phrase.find(' ')

		phrase = "https://www." + phrase.lower()
		
		# if phrase does not end with .com or other suffix, append .com to end
		if phrase.find('.com') == -1 \
			and phrase.find('.edu') == -1 \
			and phrase.find('.org') == -1:
			phrase = phrase + ".com"

		# test website existence, return "" if website doesn't exist
		try:
			phrase = phrase.lower()
			code = urllib2.urlopen(phrase).code
			if (code / 100 >= 4):
				return ""
			else:
				return phrase
		except urllib2.URLError as err: pass
		return ""

