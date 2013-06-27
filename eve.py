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

	# NOTE current functionality does not require for loop
	if opts == []:
		start_julius_listening("voice")
	else:
		for opt in opts:
			opt = opt[0]
			if opt == '-h':
				usage()
			elif opt == '-s':	
				start_julius_listening("cmdline")

			# break will be removed when/if greater functionality 
			# with cmdline args is required. 
			break

def start_julius_listening(inputMode):
	cmd = Brain()

	proc = subprocess.Popen(['padsp', 'julius', '-quiet', 
			'-input', 'mic', 
			'-C', JULIUS_FILE], 
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

def usage():
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
	
	
