#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk.gdk
import os

class Screenshot:
	def __init__(self, tts):
		self.w = gtk.gdk.get_default_root_window()
		self.size = self.w.get_size()
		self.tts = tts

	def take(self):
		pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,self.size[0],self.size[1])
		pb = pb.get_from_drawable(self.w,self.w.get_colormap(),0,0,0,0,self.size[0],self.size[1])
		if (pb != None):
			name = "screenshot.jpeg"
			# TODO:
			# search directory and see if screenshot.jpeg exists
			# if it does, change name
			done = False
			while not done:
				if os.path.isfile(name):
					# check name of screenshot 
					# if char after screenshot != digit, insert digit
					# else get digit and increment
					print name[10]
					if name[10].isdigit():
						num = int(name[10]) + 1
						name = name[:10] + str(num) + name[11:]
					else:
						name = name[:10] + "1." + name[11:] 
				else:
					done = True

			pb.save(name,"jpeg")
			self.tts.say("Screenshot saved.")
			print "screenshot saved to Jarvis folder."
		else:
			self.tts.say("Unable to get screenshot.")