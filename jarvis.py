#!/usr/bin/python
# -*- coding: utf-8 -*-

from inputs.microphone import Microphone
from ex.exception import NotUnderstoodException

import tospeech
import totext

class Job:
	def __init__(self, raw):
		self.raw_text = raw
		self.is_processed = False

	def get_is_processed(self):
		return self.is_processed

	def raw(self):
		return self.raw_text

	#natural language?


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
		#job = Job(recorded_text)

		# parse commands 
		#print recorded_text.split(' ')[0]
		first_word = recorded_text.split(' ')[0] 
		if first_word is "open":
			print "dummy"
			# facebook, google, youtube
			# if there is a second word
			# what if there is no first word?
		elif first_word is "play":
			# grooveshark
			print "dummy"
		else:
			# query wolfram alpha
			print "dummy"

		# handle errors
		if not job.get_is_processed:
			speaker.say("Sorry, I couldn't find any results for the query.")

	except NotUnderstoodException:
		speaker.say("Sorry, I couldn't understand what you said.")

if __name__ == "__main__":
	main()

	



