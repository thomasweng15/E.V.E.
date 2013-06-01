#!/usr/bin/python
# -*- coding: utf-8 -*-

from brain.command import CommandAndControl

import subprocess
import sys
import os


def main(inputMode):
	print "Loading..."
	cmd = CommandAndControl()

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
		while 1: 
			inp = "sentence1: <s> " + raw_input("> ") + " </s>"
			cmd.get_input(inp)

def print_help():
	print "Usage: python eve.py [options]"
	print "Options:"
	print "  -s       Read from stdin instead of using julius."
	print "  -n       Clear AI memory of past conversations (start new session)"
	print "  -help    Print this message and exit."
	print
	print "Please report bugs to thomasweng15 on github.com"


if __name__ == '__main__':
	if len(sys.argv) == 1:
		main("voice")
		
	elif len(sys.argv) == 2 and sys.argv[1] == "-s":
		print "Standard input mode."
		main("cmdline")

	elif len(sys.argv) == 2 and sys.argv[1] == "-n":
		if os.path.exists("./brain/Memory.ses") == True:
			os.remove("./brain/Memory.ses")
			print "AI memory erased."
		else:
			print "Warning: AI memory already doesn't exist, no memory erased."

	elif len(sys.argv) == 2 and sys.argv[1] == "-help":
		print_help()
		sys.exit(1)

	else:
		sys.exit('Error: Invalid arguments. \
			Use the \'-help\' option to learn more.')
	
