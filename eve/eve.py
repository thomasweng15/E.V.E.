#!/usr/bin/python
# -*- coding: utf-8 -*-

# padsp julius -quiet -input mic -C ./julius/julian.jconf 2>/dev/null | eve.py

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


class CommandAndControl:
	def __init__(self, file_object):
		startstring = 'sentence1: <s> '
		endstring = ' </s>'

		while 1:
			line = file_object.readline()

			if not line:
				break

			if 'missing phones' in line.lower():
				print 'Error: Missing phonemes for the used grammar file.'
				sys.exit(1)

			if line.startswith(startstring) and line.strip().endswith(endstring):
				self.parse(line.strip('\n')[len(startstring):-len(endstring)])

	def parse(self, line):
		params = [param.lower() for param in line.split() if param]
		if params == ['okaycomputer']:

			listen()
		
		elif params == ['thank', 'you', 'eve']:

			tts.Google().say("My pleasure!") # turn into wav

		#elif params == ['open', 'the', 'pod', 'bay', 'doors', 'eve']

		elif params == ['shut', 'down', 'program']:

			print "Eve will go to sleep now. Good bye!"
			tts.Google().play_wav("./eve/wav/sleep.wav")
			print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" 
			print "++++++++++++++++++++++  E.V.E. HAS SHUT DOWN  ++++++++++++++++++++++++"
			print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
			sys.exit(1) # note: doesn't exit julius speech listener


class Job:
	def __init__(self, raw):
		self.raw_text = raw
		self.is_processed = False

	def get_is_processed(self):
		return self.is_processed

	def raw(self):
		return self.raw_text


def listen():
	print "Initializing..."
	speaker = tts.Google()
	
	if not internet_on():
		print("No Internet connection.")
		speaker.play_wav("./eve/wav/internet_err.wav")
		return

	speaker.play_wav("./eve/wav/yes.wav")

	try:
		audioInput = Microphone()
		audioInput.listen()

		speaker.play_wav("./eve/wav/recd.wav")
 
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
		if first_word == "stop" or first_word == "no" or recorded_text.find('no stop') != -1:

			print "Accidental recording."
			speaker.play_wav("./eve/wav/sorry.wav")
			return

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

			speaker.play_wav("./eve/wav/query_wolfram.wav")
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
	except Exception as err: pass
	return False


if __name__ == '__main__':
	CommandAndControl(sys.stdin)


