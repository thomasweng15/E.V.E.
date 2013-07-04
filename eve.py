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
		start_julius_listening()
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

def start_julius_listening():
	"""Initialize the program and start listening for activation commands."""
	brn = Brain()
	julius_proc = subprocess.Popen(['padsp', 'julius', '-quiet', 
			'-input', 'mic', 
			'-C', JULIUS_FILE], 
			stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	while 1: 
		julius_output = julius_proc.stdout.readline()
		if brn.process_input(julius_output, julius_proc) == True:
			julius_proc = subprocess.Popen(['padsp', 'julius', '-quiet', 
				'-input', 'mic', 
				'-C', JULIUS_FILE], 
				stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		sys.stdout.flush()

def start_text_prompt():
	"""Initialize the program and open text prompt for activation commands."""
	brn = Brain()
	julius_proc = None
	print "Starting standard input mode."
	while 1:
		user_input = "sentence1: <s> " + raw_input("> ") + "</s>"
		brn.process_input(user_input, julius_proc)

def usage():
	"""Print usage / help message."""
	usage = """
		Usage: python eve.py [options]

		-h		Prints this message and exits.
		-s		Reads from stdin instead of using Julius for activation.

		Please report bugs to thomasweng15 on github.com.
	"""
	print usage
	sys.exit(1)


if __name__ == '__main__':
	main()
	
	
