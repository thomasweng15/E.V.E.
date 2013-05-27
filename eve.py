#!/usr/bin/python
# -*- coding: utf-8 -*-

from listen import listen

import tts 
import urllib2
import subprocess
import sys
import aiml # Artificial Intelligence

class CommandAndControl:
	def __init__(self):
		self.AI = aiml.Kernel()
		self.AI.setBotPredicate("name", "EVE") 
		self.AI.bootstrap(brainFile = "standard.brn")

		print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		print "++++++++++++++++++++++++  Welcome to E.V.E.  +++++++++++++++++++++++++"
		print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		print "+                                                                    +"
		print "+                    Say 'okay computer' to start!                   +"
		print "+                                                                    +"
		print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

		print "Saying: Hello there!"
		self.speaker = tts.Google()
		self.speaker.play_wav("./wav/hello.wav")

	def getInput(self, ln):

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

		elif params == ['shut', 'down', 'program']:

			print "Saying: Eve will go to sleep now. Good bye!"
			self.speaker.play_wav("./wav/sleep.wav")
			sys.exit('++++++++++++++++++++++  E.V.E. HAS SHUT DOWN  ++++++++++++++++++++++++') 

def internet_on():
	try: 
		response = urllib2.urlopen('http://173.194.33.1',timeout=1)
		return True
	except Exception as err: pass
	return False

def main(inputMode):
	print "Loading..."

	cmd = CommandAndControl()

	proc = subprocess.Popen(['padsp', 'julius', '-quiet', 
			'-input', 'mic', 
			'-C', './julius/julian.jconf'], 
			stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	if inputMode == "voice":
		while 1: 
			juliusOutput = proc.stdout.readline()
			cmd.getInput(juliusOutput)
			sys.stdout.flush()
	else:
		while 1: 
			inp = "sentence1: <s> " + raw_input("> ") + " </s>"
			cmd.getInput(inp)

def printHelp():
	print "Usage: python eve.py [options]"
	print "Options:"
	print "  -s               Read from stdin instead of using a mic."
	print "  -help            Print this message and exit."
	print
	print "Please report bugs to thomasweng15 on github.com"


if __name__ == '__main__':
	if len(sys.argv) == 1:
		main("voice")
		
	elif len(sys.argv) == 2 and sys.argv[1] == "-s":
		print "Standard input mode."
		main("cmdline")

	elif len(sys.argv) == 2 and sys.argv[1] == "-help":
		printHelp()
		sys.exit(1)

	else:
		sys.exit('Error: Invalid arguments. Use the \'-help\' option to learn more.')
	
