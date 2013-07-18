#!/usr/bin/python
# -*- coding: utf-8 -*-

from brain.brain import Brain
import getopt

import subprocess
import sys

JULIUS_FILE = "./data/julius/julian.jconf"

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hs",)
	except getopt.GetoptError:
		usage()

	# NOTE current functionality does not require for loop
	if opts == []:
		start_listening()
	else:
		for opt in opts:
			opt = opt[0]
			if opt == '-h':
				usage()
			elif opt == '-s':	
				start_text_prompt()

			# break will be removed when/if greater functionality 
			# with cmdline args is required. 
			break

def start_listening():
	"""Initialize the program and start listening for activation commands."""
	brn = Brain()
	proc = subprocess.Popen(['padsp', 'julius', '-quiet', 
			'-input', 'mic', 
			'-C', JULIUS_FILE], 
			stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	while 1: 
		line = proc.stdout.readline()
		if brn.process_input(line, proc) == True:
			proc = subprocess.Popen(['padsp', 'julius', '-quiet', 
				'-input', 'mic', 
				'-C', JULIUS_FILE], 
				stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		sys.stdout.flush()

def start_text_prompt():
	"""Initialize the program and open text prompt for activation commands."""
	brn = Brain()
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


if __name__ == '__main__':
	main()
	
	
