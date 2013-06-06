#!/usr/bin/python
# -*- coding: utf-8 -*-

from brain import listen

import tts
import sys
import urllib2
import aiml # AI
import marshal # for AI persistence


class CommandAndControl:
	def __init__(self):
		self.AI = aiml.Kernel()
		self.AI.bootstrap(brainFile = "./brain/standard.brn")
		try:
			sessionFile = open("./brain/Memory.ses", "rb")
			session = marshal.load(sessionFile)
			sessionFile.close()
			for pred,value in session.items():
				self.AI.setPredicate(pred, value, "Memory")
		except Exception:
			self.AI._addSession("Memory") 

		print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		print "+++++++++++++++++++++  Welcome to E.V.E.  ++++++++++++++++++++++"
		print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		print "+                                                              +"
		print "+                 Say 'okay computer' to start!                +"
		print "+                                                              +"
		print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

		print "Saying: Hello there!"
		self.speaker = tts.Google()
		self.speaker.play_wav("./wav/hello.wav")

	def get_input(self, ln):
		startstring = 'sentence1: <s> '
		endstring = ' </s>'

		line = ln
		if not line:
			return

		if 'missing phones' in line.lower():
			sys.exit('Error: Missing phonemes for the used grammar file.')

		if line.startswith(startstring) and line.strip().endswith(endstring):
			self.parse(line.strip('\n')[len(startstring):-len(endstring)])

	def parse(self, line):
		params = [param.lower() for param in line.split() if param]
		if params == ['okaycomputer']:
			print "Initializing..."
			if internet_on():
				listen.Listen(self.AI)
			else:
				print "Saying: No Internet connection."
				self.speaker.play_wav("./wav/internet_err.wav")
				return
		
		elif params == ['thanks', 'darling']:
			print "Saying: My pleasure."
			self.speaker.play_wav("./wav/mypleasure.wav")

		elif params == ['computer', 'power', 'down']:
			session = self.AI.getSessionData("Memory")
			sessionFile = open("./brain/Memory.ses", "wb")
			marshal.dump(session, sessionFile)
			sessionFile.close()

			#print "Saying: Eve will go to sleep now. Good bye!"
			self.speaker.play_wav("./wav/sleep.wav")
			sys.exit('+++++++++++++++++++++  E.V.E. HAS SHUTDOWN  ++++++++++++++++++++') 


def internet_on():
	try: 
		response = urllib2.urlopen('http://173.194.33.1',timeout=1)
		return True
	except Exception as err: pass
	return False