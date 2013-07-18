#!/usr/bin/python
# -*- coding: utf-8 -*-

from brain.brain import Brain
import getopt

import subprocess
import sys

LM = "./data/pocketsphinx/3178.lm"
DICT = "./data/pocketsphinx/3178.dic"

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

	psphinx_proc = subprocess.Popen(['pocketsphinx_continuous', 
			'-lm', LM, '-dict', DICT], 
			stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	while 1: 
		psphinx_output = psphinx_proc.stdout.readline().rstrip('\n')
		if brn.process_input(psphinx_output[11:], psphinx_proc) == True:
			psphinx_proc = subprocess.Popen(['pocketsphinx_continuous', 
				'-lm', LM, '-dict', DICT], 
				stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		sys.stdout.flush()

def start_text_prompt():
	"""Initialize the program and open text prompt for activation commands."""
	brn = Brain()
	psphinx_proc = None
	print "Starting standard input mode."
	while 1:
		user_input = raw_input("> ")
		brn.process_input(user_input, psphinx_proc)

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
	
	
