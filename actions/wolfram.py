#!/usr/bin/python
# -*- coding: utf-8 -*-

import wolframalpha
import webbrowser

class Wolfram:
	def __init__(self, tts, key):
		self.tts = tts
		self.key = key

	def process(self, job):
		if job.get_is_processed(): 
			return False

		if not self.key:
			self.tts.say("Please provide an API key to query Wolfram Alpha.")
			return False

		resp = self.query(job.raw(), self.key)
		self.tts.say(resp)
		
		if resp.find('No results found for') != -1:
			return False

		# open wolfram alpha page if image
		if resp == "Pulling up visual.":
			self.open(False, job.raw())
			return True

		job.is_processed = True
		return True

	def query(self, phrase, key):
		client = wolframalpha.Client(key)
		res = client.query(phrase)

		# Parse response
		try: 
			if len(res.pods) == 0:
				raise StopIteration()
			for pod in res.results:
				if hasattr(pod.text, "encode"):
					return "The answer is " + \
						pod.text.replace("°", ' degrees ')\
						.encode('ascii', 'ignore')
				else:
					break
			return "Pulling up visual."
		except StopIteration:
			return "No results found for '" + phrase + ".'"

	def say(self, text):
		return self.tts.say(text)

	def open(self, wolfram, text):
		if wolfram == True: # remove "wolfram" from start of query if it exists
			text = text[7:]

		controller = webbrowser.get()
		wolfram_url = "http://www.wolframalpha.com/input/?i="
		url = wolfram_url + text.replace(" ", "+")
		controller.open(url)
