#!/usr/bin/python
# -*- coding: utf-8 -*-

from brain.brain import Brain
import getopt

import subprocess
import sys
import os


def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "nhs",)
	except getopt.GetoptError:
		usage()

	# NOTE current functionality does not require for loop
	if opts == []:
		start_julius_listening("voice")
	else:
		# NOTE current functionality does not require for loop
		for opt in opts:
			opt = opt[0]
			if opt == '-h':
				usage()
			elif opt == '-n':
				erase_ai_memory()
			elif opt == '-s':
				start_julius_listening("cmdline")

			# break will be removed when/if greater functionality 
			# with cmdline args is required. 
			break

def start_julius_listening(inputMode):
	cmd = Brain()

	proc = subprocess.Popen(['padsp', 'julius', '-quiet', 
			'-input', 'mic', 
			'-C', './julius/julian.jconf'], 
			stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	if inputMode == "voice":
		while 1: 
			juliusInp = proc.stdout.readline()
			cmd.get_input(juliusInp)
			sys.stdout.flush()
	else:
		print "Starting standard input mode."
		while 1: 
			inp = "sentence1: <s> " + raw_input("> ") + " </s>"
			cmd.get_input(inp)

def erase_ai_memory():
	try:
		os.remove("./brain/Memory.ses")
		sys.exit("AI memory successfully erased.")
	except IOError:
		sys.exit("Warning: AI memory cannot be found, no memory erased.")

def usage():
	usage = """
	Usage: python eve.py [options]

	-h		Prints this message and exits.
	-n		Clears AI memory of past conversations (starts new session)
	-s		Reads from stdin instead of using Julius for activation.

	Please report bugs to thomasweng15 on github.com.
	"""
	print usage
	sys.exit(1)


if __name__ == '__main__':
	main()
	
	
