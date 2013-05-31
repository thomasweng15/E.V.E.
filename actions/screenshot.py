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
			while 1: # check if name exists - change if already exists
				if os.path.isfile(name): 
					if name[10].isdigit():
						num = int(name[10]) + 1
						name = name[:10] + str(num) + name[11:]
					else:
						name = name[:10] + "1." + name[11:] 
				else:
					break

			pb.save(name,"jpeg")
			self.tts.say("Screenshot saved.")
			print "Screenshot saved to E.V.E. folder."

		else:
			self.tts.say("Unable to get screenshot.")
			print "Screenshot failed."