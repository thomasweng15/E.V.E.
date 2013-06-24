#!/usr/bin/python
# -*- coding: utf-8 -*-

from voicecmd import VoiceCommand
from inputs.microphone import Microphone
from ex.exception import NotUnderstoodException
from ex.exception import ConnectionLostException

import tts
import stt
import sys
import urllib2
import aiml # AI
import marshal # for AI persistence


class Job:
	"""
	stores text converted from recorded voice input, 
	and a boolean describing the job's state of whether 
	or not it has been processed. Job instances are 
	processed through the VoiceCommand class.
	"""
	def __init__(self, recorded_text):
		self.recorded_text = recorded_text
		self.query = ""
		self.is_processed = False

	def get_is_processed(self):
		return self.is_processed

	def recorded(self):
		return self.recorded_text

	def set_query(self, query):
		self.query = query

	def query(self):
		return self.query


class Brain:
	"""
	initializes everything EVE needs to function, 
	listens for activation input from julius, 
	and executes commands based on voice input.
	The Brain class coordinates all other components
	of EVE.
	"""
	def __init__(self):
		self.audioInput = Microphone()
		self.speaker = tts.Google()
		self.voice_cmd = VoiceCommand(self.speaker)
		self._load_ai() 
		self._print_welcome()

		print "Saying: Hello there!"
		self.speaker.play_wav("./wav/hello.wav")

	def _load_ai(self):
		self.AI = aiml.Kernel()
		self.AI.bootstrap(brainFile = "./brain/standard.brn")
		try:
			sessionFile = open("./brain/Memory.ses", "rb")
			session = marshal.load(sessionFile)
			sessionFile.close()
			for pred,value in session.items():
				self.AI.setPredicate(pred, value, "Memory")
		except IOError:
			self.AI._addSession("Memory")

	def _print_welcome(self):
		print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		print "+++++++++++++++++++++  Welcome to E.V.E.  ++++++++++++++++++++++"
		print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		print "+                                                              +"
		print "+                 Say 'okay computer' to start!                +"
		print "+                                                              +"
		print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

################################################################################

	def get_input(self, ln):
		startstring = 'sentence1: <s> '
		endstring = ' </s>'

		line = ln
		if not line:
			return

		if 'missing phones' in line.lower():
			sys.exit('Error: Missing phonemes for the used grammar file.')

		if line.startswith(startstring) and line.strip().endswith(endstring):
			self.parse(line.strip('\n')[len(startstring):-len(endstring)])

	def parse(self, line):
		params = [param.lower() for param in line.split() if param]
		if params == ['okaycomputer']:
			self._okaycomputer()
		
		elif params == ['thanks', 'darling']:
			self._thanks()

		elif params == ['computer', 'power', 'down']:
			self._shutdown()

	def _okaycomputer(self):
		print "Initializing..."
		if self._internet_on():
			self.listen()
		else:
			print "Saying: No Internet connection."
			self.speaker.play_wav("./wav/internet_err.wav")
			return

	def _internet_on(self):
		try: 
			response = urllib2.urlopen('http://google.com',timeout=1)
			return True
		except urllib2.URLError:
			return False

	def _thanks(self):
		print "Saying: My pleasure."
		self.speaker.play_wav("./wav/mypleasure.wav")

	def _shutdown(self):
		session = self.AI.getSessionData("Memory")
		sessionFile = open("./brain/Memory.ses", "wb")
		marshal.dump(session, sessionFile)
		sessionFile.close()
		print "Saying: E.V.E. will go to sleep now. Good bye!"
		self.speaker.play_wav("./wav/sleep.wav")
		sys.exit('+++++++++++++++++++++  E.V.E. HAS SHUTDOWN  ++++++++++++++++++++') 

################################################################################

	def listen(self):
		print "Saying: Yes?"
		self.speaker.play_wav("./wav/yes.wav")

		self.audioInput.listen() # listen to mic and record
		job = self._set_job()
		if job is not None:
			self._parse_input(job)

	def _set_job(self):
		speech_to_text = stt.Google(self.audioInput)
		try:
			recorded_text = speech_to_text.get_text().lower()
			return Job(recorded_text)
		except NotUnderstoodException:
			print "Sorry, I didn't get that."
			self.speaker.play_wav("./wav/didntget.wav")
			return None
		except ConnectionLostException:
			print "Sorry, the internet connection failed."
			self.speaker.play_wav("./wav/conn_failed.wav")
			return None

	def _parse_input(self, job):
		t_keys = ['google', 'youtube', 'search', 'open', 'computer', 'play', 'video']
		i_keys = ['news','screenshot']
		action_verbs = ['search', 'look', 'pull', 'get']
		prepositions = ['for', 'on', 'of']

		action_verb = "" 
		command_type = ""
		t_key = "" 
		i_key = ""
		preposition = ""
		query = ""

		words = job.recorded().split()

		for word in words:
			# set action verb if it comes before any other goalpost
			if word in action_verbs and action_verb == "" and t_key == "":
				action_verb = word 
			# set t_key if it comes before any other t_key
			elif word in t_keys and t_key == "":
				t_key = word
				command_type = word
			# set i_key if it comes before any other key
			elif word in i_keys and t_key == "" and i_key == "":
				i_key = word
				command_type = word
			# find prepositions in cases such as "youtube video of" or "google for"
			elif word in prepositions and t_key != "":
				preposition = word
			# catch the stop recording case
			elif word == "no" and words[words.index(word) + 1] == "stop":
				print "Accidental recording"
				command_type = "no stop"
				break

		if command_type not in i_key: # then a query exists.
			if preposition == "":
				query_list = words[words.index(command_type) + 1:]
			else:
				query_list = words[words.index(preposition) + 1:]

			query = ' '.join(query_list)
			job.set_query(query)
		
		self._execute_voice_cmd(job, command_type, query)

	def _execute_voice_cmd(self, job, command_type, query):
		if command_type == "no stop":
			self.voice_cmd.accidental_recording()

		elif command_type == "open":
			if query != "":
				self.voice_cmd.open_webpage(job)
			else:
				self.speaker.say("no webpage specified.")

		elif command_type == "google" or command_type == "search":
			if query != "":
				self.voice_cmd.google(job)
			else: 
				self.speaker.say("no query provided.")

		elif command_type == "youtube":
			if query != "":
				# TODO there are flaws with this method of differentiating
				# between search and play for youtube. Improve method.
				if job.recorded().find('search') != -1: 
					self.voice_cmd.search_youtube(job)
				else: 
					self.voice_cmd.play_youtube(job)
			else:
				self.speaker.say("no query provided.")

		elif command_type == "screenshot": 
			self.voice_cmd.take_screenshot()

		elif command_type == "computer":
			self.voice_cmd.ai_respond(job, self.AI, "Memory")

		# TODO refactor to conform to new standard
		elif job.recorded().find('change news source') != -1:
			self.voice_cmd.change_news_source(job)

		elif command_type == "news": # get news
			self.voice_cmd.get_news(job)

		elif command_type == "play":
			self.voice_cmd.play_music(job)

		else:
			self.voice_cmd.ask_wolfram(job)


		if not job.get_is_processed:
			self.speaker.say("Sorry, I didn't find any results.")












