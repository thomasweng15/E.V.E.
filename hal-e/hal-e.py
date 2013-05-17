#!/usr/bin/python
# -*- coding: utf-8 -*-

from inputs.microphone import Microphone
from ex.exception import NotUnderstoodException
from actions.wolfram import Wolfram
from actions.youtube import Youtube
from actions.screenshot import Screenshot

import urllib2
import tts
import stt
import webbrowser
import os
import sys

class Job:
	def __init__(self, raw):
		self.raw_text = raw
		self.is_processed = False

	def get_is_processed(self):
		return self.is_processed

	def raw(self):
		return self.raw_text

def main():
	print "Initializing..."
	speaker = tts.Google()

	if sys.argv[1:] == ['shutdown']:
		print "HAL-E will go to sleep now. Goodbye!"
		speaker.play_wav("./hal-e/wav/sleep.wav")
		return
	
	if not internet_on():
		print("No Internet connection.")
		speaker.play_wav("./hal-e/wav/internet_err.wav")
		return

	try:
		speaker.play_wav("./hal-e/wav/yes.wav")

		audioInput = Microphone()
		audioInput.listen()
 
		speech_to_text = stt.Google(audioInput)

		recorded_text = speech_to_text.get_text()
		job = Job(recorded_text)

		# parse first and second words in command
		first_word = (recorded_text.split(' ')[0]).lower() 
		if recorded_text.find(' ') >= 1:
			second_word = (recorded_text.split(' ')[1]).lower()
		else:
			second_word = ""

		# initialize controller for web browser
		controller = webbrowser.get()

		# execute commands based on first word in query
		if first_word == "open":

			if not second_word == "": # open webpage

				phrase = recorded_text[recorded_text.find(' ') + 1:]
				url = make_url(phrase)

				if url != "": 
					
					speaker.say("opening " + url[12:])
					controller.open(url)
				
				else: 

					speaker.say("sorry, I didn't recognize the web page.")

			else:

				speaker.say("no webpage specified.")

		elif first_word == "google": 

			if not second_word == "": # pull up query results
				
				speaker.say("searching...")
				google_url = "http://www.google.com/search?q="
				phrase = recorded_text[recorded_text.find(' ') + 1:]
				url = google_url + speaker.spacesToPluses(phrase)
				controller.open(url)

			else: # no query provided, just open google

				speaker.say("opening google.com.")
				url = "http://www.google.com"
				controller.open(url)

		elif first_word == "youtube":

			if second_word != "": 

				if second_word == "search": # return youtube search results

					speaker.say("Pulling up youtube results.")
					youtube_url = "http://www.youtube.com/results?search_query="
					phrase = recorded_text[recorded_text.find(' ') + 1:]
					phrase = phrase[recorded_text.find(' ') + 1:]
					url = youtube_url + speaker.spacesToPluses(phrase)
					controller.open(url)

				else: # open first youtube video associated with query

					speaker.say("Playing video.")
					Youtube(speaker).process(job)

			else: 

				speaker.say("Opening youtube.com.")
				url = "http://www.youtube.com"
				controller.open(url)

		elif first_word == "play" or first_word == "grooveshark":

			speaker.say("opening Grooveshark.")
			
			if not second_word == "": # pull up Grooveshark search results
				
				# TODO auto play first music item from search results
				grooveshark_url = "http://grooveshark.com/#!/search?q="
				phrase = recorded_text[recorded_text.find(' ') + 1:]
				url = grooveshark_url + speaker.spacesToPluses(phrase)
				controller.open(url)

			else:

				url = "http://grooveshark.com"
				controller.open(url)

		elif first_word == "wolfram": # pull up wolfram alpha search result

			speaker.play_wav("./hal-e/wav/query_wolfram.wav")
			Wolfram(speaker, os.environ.get('WOLFRAM_API_KEY')).open(True, recorded_text)

		elif recorded_text.lower().find('screenshot') != -1:

			Screenshot(speaker).take()

		else: # query wolfram api

			Wolfram(speaker, os.environ.get('WOLFRAM_API_KEY')).process(job)

		# handle errors
		if not job.get_is_processed:
			speaker.say("Sorry, I didn't find any results.")

	except NotUnderstoodException:
		speaker.say("Sorry, I didn't get that.")


def make_url(phrase):
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


	



