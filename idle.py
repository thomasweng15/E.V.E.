#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import subprocess
import os

JULIUS_FILE = "./data/julius/julian.jconf"

def main():
	startstring = 'sentence1: <s> '
	endstring = ' </s>'

	proc = subprocess.Popen(['padsp', 'julius', '-quiet', 
			'-input', 'mic', 
			'-C', JULIUS_FILE], 
			stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	print "Say 'computer wake up' to turn E.V.E. on."

	while 1:
		line = proc.stdout.readline().lower()

		if not line:
			continue

		if 'missing phones' in line:
			sys.exit('Error: Missing phonemes for the used grammar file.')

		if line.startswith(startstring) and line.strip().endswith(endstring):
			line = line.strip('\n')[len(startstring):-len(endstring)]
			params = line.split()
			if params == ['computer', 'wake', 'up']:
				print "Waking up..."
				proc.kill()
				os.system("python eve.py")
				sys.exit(1)

if __name__ == '__main__':
	main()
	