#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib2 import urlopen
from actions.actions_helper import ActionsHelper
import json


class Youtube:
	def __init__(self, speaker):
		self.speaker = speaker

	def process(self, job, controller):
		self.speaker.say("Playing video.")

		if job.get_is_processed():
			return False
			
		result = self.get_first_video(job.recorded(), controller)
		job.is_processed = True

	# get the URL of the first video and open in firefox
	def get_first_video(self, phrase, controller):
		y_url = "http://gdata.youtube.com/feeds/api/videos?max-results=1&alt=json&orderby=relevance&q="
		url = y_url + phrase.replace(" ", "+")
		inp = urlopen(url)
		resp = json.load(inp)
		inp.close()

		first = resp['feed']['entry'][0]
		url = first['link'][0]['href']
		if ActionsHelper().test_url(url) != "":
			controller.open(url)
		else:
			print "Error: page not found."		

	def search(self, job, controller):
		self.speaker.say("Pulling up youtube results.")
		y_url = "http://www.youtube.com/results?search_query="
		phrase = job.recorded()[job.recorded().find(' ') + 1:]
		phrase = phrase[job.recorded().find(' ') + 1:]
		url = y_url + phrase.replace(" ", "+")
		if ActionsHelper().test_url(url) != "":
			controller.open(url)
		else: 
			print "Error: page not found."


