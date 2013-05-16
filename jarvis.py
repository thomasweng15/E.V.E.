#!/usr/bin/python
# -*- coding: utf-8 -*-

from inputs.microphone import Microphone
from ex.exception import NotUnderstoodException
from actions.wolfram import Wolfram
from actions.youtube import Youtube

import urllib2
import tospeech
import totext
import webbrowser
import os

class Job:
	def __init__(self, raw):
		self.raw_text = raw
		self.is_processed = False

	def get_is_processed(self):
		return self.is_processed

	def raw(self):
		return self.raw_text

def main():
	speaker = tospeech.Google()

	# test internet connection
	if not internet_on():
		speaker.play_wav("./wavmsgs/internet_err.wav")
		return

	try:
		audioInput = Microphone()
		audioInput.listen()

		# init new Voice class associated with audio 
		speech_to_text = totext.Google(audioInput)

		# convert audio file into text and init a new Job class with text
		recorded_text = speech_to_text.get_text()
		job = Job(recorded_text)

		# parse commands 
		first_word = recorded_text.split(' ')[0] 
		second_word = ""

		if recorded_text.find(' ') >= 1:
			second_word = recorded_text.split(' ')[1]

		controller = webbrowser.get('firefox')

		if first_word == "open":

			if not second_word == "":

				phrase = recorded_text[recorded_text.find(' ') + 1:]
				url = make_url(phrase)

				if url != "":
					
					print url[11:]
					speaker.say("opening " + url)

					controller.open(url)
				
				else: 

					speaker.say("sorry, I did not recognize the web page.")

			else:

				speaker.say("no webpage specified.")

		elif first_word == "Google":

			speaker.say("opening google.com.")

			if not second_word == "":
				
				# pull up google search results 
				google_url = "http://www.google.com/search?q="
				phrase = recorded_text[recorded_text.find(' ') + 1:]
				url = google_url + speaker.spacestoPluses(phrase)

			else:

				url = "http://www.google.com"

			controller.open(url)

		elif first_word == "YouTube":

			speaker.say("opening youtube.com.")

			if not second_word == "":

				# pull up youtube search results
				#youtube_url = "http://www.youtube.com/results?search_query="
				#phrase = recorded_text[recorded_text.find(' ') + 1:]
				#url = youtube_url + speaker.spacestoPluses(phrase)

				# Open first youtube video associated with job
				Youtube(speaker).process(job)

			else: 

				url = "http://www.youtube.com"
				controller.open(url)

		elif first_word == "play" or first_word == "Grooveshark":

			speaker.say("opening Grooveshark.")
			
			if not second_word == "":

				# pull up Grooveshark search results
				grooveshark_url = "http://grooveshark.com/#!/search?q="
				phrase = recorded_text[recorded_text.find(' ') + 1:]
				url = grooveshark_url + speaker.spacestoPluses(phrase)

			else:

				url = "http://grooveshark.com"

			controller.open(url)

		else:
			speaker.play_wav("./wavmsgs/query_wolfram.wav")

			# query wolfram api
			Wolfram(speaker, os.environ.get('WOLFRAM_API_KEY')).process(job)

			# pull up wolfram alpha search result
			wolfram_url = "http://www.wolframalpha.com/input/?i="
			url = wolfram_url + speaker.spacestoPluses(recorded_text)
			controller.open(url)

		# handle errors
		if not job.get_is_processed:
			speaker.say("Sorry, I couldn't find any results for the query.")

	except NotUnderstoodException:
		speaker.say("Sorry, I couldn't understand what you said.")

def make_url(phrase):
	phrase = "http://www." + phrase
	
	# if phrase does not end with .com, append to end
	# implement other types later, e.g. .edu
	if phrase.find('.com') == -1:
		phrase = phrase + ".com"

	# test website existence before returning
	try:
		phrase = phrase.lower()
		code = urllib2.urlopen(phrase).code
		if (code / 100 >= 4):
			return ""
		else:
			return phrase
	except urllib2.URLError as err:pass
	return ""

def internet_on():
	try: 
		response = urllib2.urlopen('http://173.194.33.1',timeout=1)
		return True
	except urllib2.URLError as err: pass
	return False

if __name__ == "__main__":
	main()


	



