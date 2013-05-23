#!/usr/bin/python
# -*- coding: utf-8 -*-

# padsp julius -quiet -input mic -C ./julius/julian.jconf 2>/dev/null | python eve.py

from listen import listen

import tts # could add to init and pass to other files
import urllib2
import subprocess
import sys
import aiml # Artificial Intelligence

class CommandAndControl:
	def __init__(self):
		self.AI = aiml.Kernel()
		self.AI.setBotPredicate("name", "EVE") 
		self.AI.setBotPredicate("user", "Thomas")
		self.AI.bootstrap(brainFile = "standard.brn")

		print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		print "++++++++++++++++++++++++  Welcome to E.V.E.  +++++++++++++++++++++++++"
		print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		print "+                                                                    +"
		print "+                    Say 'okay computer' to start!                   +"
		print "+                                                                    +"
		print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

		self.speaker = tts.Google()
		self.speaker.play_wav("./wav/hello.wav")

	def getInput(self, ln):

		startstring = 'sentence1: <s> '
		endstring = ' </s>'

		line = ln

		if not line:
			return

		if 'missing phones' in line.lower():
			print 'Error: Missing phonemes for the used grammar file.'
			sys.exit(1)

		if line.startswith(startstring) and line.strip().endswith(endstring):
			self.parse(line.strip('\n')[len(startstring):-len(endstring)])

	def parse(self, line):
		params = [param for param in line.split() if param]
		if params == ['OKAYCOMPUTER']:

			print "Initializing..."
			if internet_on():
				listen.Listen(self.AI)
			else:
				print "No Internet connection."
				self.speaker.play_wav("./wav/internet_err.wav")
				return
		
		elif params == ['THANKS', 'DARLING']:

			self.speaker.play_wav("./wav/mypleasure.wav")

		elif params == ['SHUT', 'DOWN', 'PROGRAM']:

			print "Eve will go to sleep now. Good bye!"
			self.speaker.play_wav("./wav/sleep.wav")
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

def main():
	print "Loading..."

	cmd = CommandAndControl()

	proc = subprocess.Popen(['padsp', 'julius', '-quiet', 
			'-input', 'mic', 
			'-C', './julius/julian.jconf'], 
			stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	while 1:
		output = proc.stdout.readline()
		cmd.getInput(output)
		sys.stdout.flush()

if __name__ == '__main__':
	main()
	
