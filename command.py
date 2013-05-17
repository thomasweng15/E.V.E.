#! /usr/bin/python -u
#
# How to use it:
#  padsp julius -quiet -input mic -C ./julius/julian.jconf 2>/dev/null | python command.py
# 	padsp may not be necessary.

import sys 
import os

class CommandAndControl:
	def __init__(self, file_object):
		startstring = 'sentence1: <s> '
		endstring = ' </s>'

		while 1:

			line = file_object.readline()

			if not line:
				
				break

			if 'missing phones' in line.lower():
				
				print 'Error: Missing phonemes for the used grammar file.'
				sys.exit(1)

			if line.startswith(startstring) and line.strip().endswith(endstring):
				
				self.parse(line.strip('\n')[len(startstring):-len(endstring)])

	def parse(self, line):
		# Parse the input
		params = [param.lower() for param in line.split() if param]
		# Execute command
		if params == ['okay', 'jarvis']:
			os.system("python ./jarvis/jarvis.py")

if __name__ == '__main__':
	try:
		CommandAndControl(sys.stdin)
	except KeyboardInterrupt:
		sys.exit(1)


