#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk.gdk
import os
import sys


DATAFILE = "./data/user_config.txt"

class Screenshot:
	"""
	Process jobs requesting a screenshot.
	
	"""
	def __init__(self, speaker):
		self.w = gtk.gdk.get_default_root_window()
		self.size = self.w.get_size()
		self.speaker = speaker
		self.get_screenshot_dir()

	def take(self):
		"""Take a screenshot and store it."""
		pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,self.size[0],self.size[1])
		pb = pb.get_from_drawable(self.w,self.w.get_colormap(),0,0,0,0,self.size[0],self.size[1])
		
		if (pb != None):
			name = "screenshot.jpeg"
			while 1: # check if name exists - change if already exists
				if os.path.isfile(self.screenshot_dir + name): 
					if name[10].isdigit():
						num = int(name[10]) + 1
						name = name[:10] + str(num) + name[11:]
					else:
						name = name[:10] + "1." + name[11:] 
				else:
					break

			pb.save(self.screenshot_dir + name,"jpeg")
			self.speaker.say("Screenshot saved.")
			print "Screenshot saved to '" + self.screenshot_dir + "' folder."

		else:
			self.speaker.say("Unable to get screenshot.")
			print "Screenshot failed."

	def get_screenshot_dir(self):
		"""Find screenshot directory from datafile."""
		try:
			f = open(DATAFILE, 'r')
		except IOError:
			self.speaker.say("Error, datafile cannot be found.")
			sys.exit(1)

		found_screenshot_dir = False
		for line in f:
			if line.find("screenshot_dir::") != -1:
				self.screenshot_dir = line[len("screenshot_dir::"):].rstrip('\n')
				found_screenshot_dir = True
				break

		if found_screenshot_dir != True:
			self.speaker.say("Oops, datafile does not contain screenshot directory item.")
		f.close()