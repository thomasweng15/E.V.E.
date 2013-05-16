#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import webbrowser
from urllib2 import urlopen

class Youtube:
	def __init__(self, tospeech):
		self.tospeech = tospeech

	def process(self, job):
		if job.get_is_processed():
			return False

		result = self.getFirstVideo(job.raw())
		job.is_processed = True

	# get the URL of the first video and open in firefox
	def getFirstVideo(self, phrase):
		youtube_url = "http://gdata.youtube.com/feeds/api/videos?max-results=1&alt=json&orderby=relevance&q="
		youtube_url = youtube_url + self.tospeech.spacestoPluses(phrase)
		inp = urlopen(youtube_url)
		resp = json.load(inp)
		inp.close()

		first = resp['feed']['entry'][0]

		controller = webbrowser.get('firefox')
		controller.open(first['link'][0]['href'])

		return 


