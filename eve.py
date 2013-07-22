#!/usr/bin/python
# -*- coding: utf-8 -*-

from brain.brain import Brain
import getopt

import subprocess
import sys
import os

JULIUS_FILE = "./data/julius/julian.jconf"

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hs",)
	except getopt.GetoptError:
		usage()

	brain = Brain()
	print_welcome()

	# NOTE current functionality does not require for loop
	if opts == []:
		start_listening(brain)
	else:
		for opt in opts:
			opt = opt[0]
			if opt == '-h':
				usage()
			elif opt == '-s':	
				start_text_prompt(brain)

			# break will be removed when/if greater functionality 
			# with cmdline args is required. 
			break


def start_listening(brain):
	"""Initialize the program and start listening for activation commands."""
	startstring = 'sentence1: <s> '
	endstring = ' </s>'

	proc = subprocess.Popen(['padsp', 'julius', '-quiet', 
			'-input', 'mic', 
			'-C', JULIUS_FILE], 
			stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	while 1: 
		line = proc.stdout.readline().lower()

		if 'missing phones' in line:
			sys.exit('Error: Missing phonemes for the used grammar file.')

		if line.startswith(startstring) and line.strip().endswith(endstring):
			phrase = line.strip('\n')[len(startstring):-len(endstring)]
			if parse(phrase, proc, brain) == True:
				proc = subprocess.Popen(['padsp', 'julius', '-quiet', 
					'-input', 'mic', 
					'-C', JULIUS_FILE], 
					stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

		sys.stdout.flush()
		

def parse(phrase, proc, brain):
	"""
	Identify activation commands from input 
	extracted by the 'process_input' function and
	call the appropriate function for a given command.
	
	"""
	params = phrase.split()
	if params == ['okay', 'computer']:
		if proc is not None:
			proc.kill()
		brain.okaycomputer()

	elif params == ['computer', 'lets', 'talk']:
		if proc is not None:
			proc.kill()
		brain.conversation()

	elif params == ['computer', 'shut', 'down']:
		if proc is not None:
			proc.kill()
		shutdown(brain)

	elif params == ['computer', 'go', 'sleep']:
		if proc is not None:
			proc.kill()
		sleep(brain)
	else: 
		return False

	return True


def start_text_prompt(brn):
	"""Initialize the program and open text prompt for activation commands."""
	
	print "Starting standard input mode."
	while 1:
		line = raw_input("> ")
		brn.process_input(line, None)


def usage():
	"""Print usage / help message."""
	usage = """
		Usage: python eve.py [options]

		-h		Prints this message and exits.
		-s		Reads from stdin instead of using pocketsphinx for activation.

		Please report bugs to thomasweng15 on github.com.
	"""
	print usage
	sys.exit(1)


def print_welcome():
	"""
	Print welcome message in terminal when E.V.E. first starts up
	and initializes the Brain class.
	
	"""
	welcome_message =  """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++  Welcome to E.V.E.  ++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                                                              +
+                 Say 'okay computer' to start!                +
+                                                              +
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	"""
	print welcome_message


def shutdown(brain):
	"""Close the E.V.E. program."""
	# TODO turn into local wav file
	brain.speaker.say("E.V.E. will shut down now. Goodbye!")
	sys.exit('+++++++++++++++++++++  E.V.E. HAS SHUTDOWN  ++++++++++++++++++++')
	

def sleep(brain):
	"""Puts E.V.E. to sleep."""
	brain.speaker.say("E.V.E. will go to sleep now. Wake me when you need me!")
	print('+++++++++++++++  E.V.E. IS IN SLEEP MODE  ++++++++++++++')
	os.system("python idle.py")
	sys.exit(1) # does this script terminate before idle.py terminates?


if __name__ == '__main__':
	main()
	
	
