#! /usr/bin/python -u

# padsp julius -quiet -input mic -C ./julius/julian.jconf 2>/dev/null | command.py

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
		params = [param.lower() for param in line.split() if param]
		if params == ['okay', 'hal-e']:

			os.system("python ./hal-e/hal-e.py")
		
		elif params == ['shut', 'down', 'program']:

			os.system("python ./hal-e/hal-e.py shutdown")
			os.system("echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
			os.system("echo ++++++++++++++++++  HAL-E HAS SHUT DOWN  +++++++++++++++++++")
			os.system("echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
			sys.exit(1) # note: doesn't exit julius speech listener

if __name__ == '__main__':
	CommandAndControl(sys.stdin)


