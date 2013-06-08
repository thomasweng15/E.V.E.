#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib2 import urlopen
import json


class Youtube:
	def __init__(self, tts):
		self.tts = tts

	def process(self, job, controller):
		if job.get_is_processed():
			return False

		result = self.get_first_video(job.recorded(), controller)
		job.is_processed = True

	# get the URL of the first video and open in firefox
	def get_first_video(self, phrase):
		y_url = "http://gdata.youtube.com/feeds/api/videos?max-results=1&alt=json&orderby=relevance&q="
		url = y_url + phrase.replace(" ", "+")
		inp = urlopen(url)
		resp = json.load(inp)
		inp.close()

		first = resp['feed']['entry'][0]

		controller.open(first['link'][0]['href'])


