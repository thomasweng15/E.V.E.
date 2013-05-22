#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

def main():
	print "Loading..."

	os.system("padsp julius -quiet -input mic -C ./julius/julian.jconf 2>/dev/null | python eve.py")
    
if __name__ == '__main__':
	main()