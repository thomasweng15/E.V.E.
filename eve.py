#!/usr/bin/python
# -*- coding: utf-8 -*-

# padsp julius -quiet -input mic -C ./julius/julian.jconf 2>/dev/null | eve.py

import tts
from listen import listen

import urllib2
import os
import sys

class CommandAndControl:
	def __init__(self, file_object):
		self.speaker = tts.Google()
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
		params = [param for param in line.split() if param]
		if params == ['OKAYCOMPUTER']:

			if internet_on():
				listen.Listen()
			else:
				print "No Internet connection."
				self.speaker.play_wav("./wav/internet_err.wav")
		
		elif params == ['THANK', 'YOU', 'EVE']:

			self.speaker.say("My pleasure!") # turn into wav

		elif params == ['TESTINTERNET']:

			if internet_on():
				self.speaker.play_wav("./wav/connected.wav")
			else:
				print "No Internet connection."
				self.speaker.play_wav("./wav/internet_err.wav")

		#elif params == ['open', 'the', 'pod', 'bay', 'doors', 'eve']

			#tts.Google().say("Sorry, Dave, I'm afraid I can't do that.")

		elif params == ['EVE', 'SHUT', 'DOWN':

			print "Eve will go to sleep now. Good bye!"
			self.speaker.play_wav("./eve/wav/sleep.wav")
			print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" 
			print "++++++++++++++++++++++  E.V.E. HAS SHUT DOWN  ++++++++++++++++++++++++"
			print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
			sys.exit(1) # note: doesn't exit julius speech listener

def internet_on():
	try: 
		response = urllib2.urlopen('http://173.194.33.1',timeout=1)
		return True
	except Exception as err: pass
	return False

if __name__ == '__main__':
	CommandAndControl(sys.stdin)
