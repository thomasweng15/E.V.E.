import gtk.gdk
import os
import sys


class Screenshot:
	"""
	Process jobs requesting a screenshot.
	
	"""
	def __init__(self, speaker, actions_helper):
		self.w = gtk.gdk.get_default_root_window()
		self.size = self.w.get_size()
		self.speaker = speaker
		self.helper = actions_helper
		self.screenshot_dir = self.helper.get_value_from_datafile("screenshot_dir")

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
