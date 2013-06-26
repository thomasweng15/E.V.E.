#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import xml.etree.ElementTree as ET
import re


class Wolfram:
	"""
	processes jobs that request to query the wolfram alpha database.
	"""

	def __init__(self, tts, key):
		self.tts = tts
		self.key = key

	def process(self, job, controller):
		if job.get_is_processed(): 
			return False

		if not self.key:
			self.tts.say("Please provide an API key to query Wolfram Alpha.")
			return False

		response = self.query(job.recorded(), self.key)
		
		if response.find('No results') != -1:
			return False
		elif response == "Pulling up visual.":
			self.tts.say(response)
			self.open(False, job.recorded(), controller)
		else:
			self.tts.say(response)

		job.is_processed = True
		return True

	def query(self, phrase, key):
		phrase = phrase.replace(' ', '%20')
		w_url = "http://api.wolframalpha.com/v2/query?input=" + phrase + "&appid=" + key
		xml_data=urllib2.urlopen(w_url).read()
		root = ET.fromstring(xml_data)

		# Parse response
		try:
			pods = root.findall('.//pod')
			
			if pods == []:
				raise StopIteration()

			# if first and second pods are input interpretation and response, stop and ignore
			if pods[0].attrib['title'] == "Input interpretation" and \
				pods[1].attrib['title'] == "Response":
				raise StopIteration()

			for pod in pods:
				# skip input human response (we are doing that ourselves) and input interpretation
				if pod.attrib['title'] != "Response" and \
					pod.attrib['title'] != "Input interpretation":
					plaintexts = pod.findall('.//plaintext')
					text = plaintexts[0].text
					if text is not None: 	
						# remove anything in parentheses
						# TODO removing things in parentheses needs to be smart
						# text = re.sub(r'\([^)]*\)', '', text)
						return "the answer is " + text.replace("°", ' degrees ')\
							.encode('ascii', 'ignore')
					else:
						return "Pulling up visual."

		except StopIteration:
			return "No results"

	def open(self, wolfram, text, controller):
		wolfram_url = "http://www.wolframalpha.com/input/?i=" + text.replace(" ", "+")
		controller.open(url)
