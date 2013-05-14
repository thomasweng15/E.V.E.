#!/usr/bin/python
# -*- coding: utf-8 -*-

from inputs.microphone import Microphone
from ex.exception import NotUnderstoodException

import tospeech
import totext
import webbrowser

class Job:
	def __init__(self, raw):
		self.raw_text = raw
		self.is_processed = False

	def get_is_processed(self):
		return self.is_processed

	def raw(self):
		return self.raw_text

	#natural language using nltk?


def main():
	speaker = tospeech.Google()

	try: 
		#while loop to listen for queries using Julius?
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
			# make it so that I can tell whether there is a webpage there or not
			# before I open the webpage.
			if not second_word == "":
				print "opening webpage"
				# get url of rest of word
				#controller.open()
			else:
				print "no webpage specified"
		elif first_word == "Google":
			# if there are more words get them
			speaker.say("opening google.com")
			# test opening just google
			url = "http://www.google.com"
			controller.open(url)
		elif first_word == "YouTube":
			speaker.say("opening youtube.com")
			# test opening just youtube
			url = "http://www.youtube.com"
			controller.open(url)
		elif first_word == "play":
			# grooveshark
			print "Grooveshark"
		else:
			# query Wolfram Alpha
			print "dummy"

		# handle errors
		if not job.get_is_processed:
			speaker.say("Sorry, I couldn't find any results for the query.")

	except NotUnderstoodException:
		speaker.say("Sorry, I couldn't understand what you said.")

if __name__ == "__main__":
	main()

	



