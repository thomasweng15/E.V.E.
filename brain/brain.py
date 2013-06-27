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
import aiml 

BRAINFILE = "./data/standard.brn"
AI_CONFIG = "./data/AI_config.txt"

# natural voice command parsing keywords
T_KEYS = ['google', 'youtube', 'search', 'open', 'computer', 'radio', 'video']
I_KEYS = ['news','screenshot']
ACTION_VERBS = ['search', 'look', 'pull', 'get', 'give']
PREPOSITIONS = ['for', 'on', 'of']


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
		self.AI.bootstrap(brainFile=BRAINFILE)
		self.ai_config()

	def ai_config(self):
		# set bot properties, such as name and favorite food
		try: 
			f = open(AI_CONFIG)
		except IOError:
			self.speaker.say("Error, artificial intelligence configuration file not found.")
			sys.exit(1)
		bot_predicates = f.readlines()
		f.close()
		for bot_predicate in bot_predicates:
			key_value = bot_predicate.split('::')
			if len(key_value) == 2:
				self.AI.setBotPredicate(key_value[0], key_value[1].rstrip('\n'))


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

		line = ln.lower()
		if not line:
			return

		if 'missing phones' in line:
			sys.exit('Error: Missing phonemes for the used grammar file.')

		if line.startswith(startstring) and line.strip().endswith(endstring):
			self.parse(line.strip('\n')[len(startstring):-len(endstring)])

	def parse(self, line):
		params = line.split()
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
			# BUG this line of code hangs when the DNS lookup is unsuccessful, 
			# while using a specific IP address does not have this problem and the 
			# connection test turns back True or False within a second. However, 
			# using a specific IP address means that some regions have trouble 
			# accessing it.
			return urllib2.urlopen('http://www.google.com',timeout=1)
		except urllib2.URLError:
			return False

	def _thanks(self):
		print "Saying: My pleasure."
		self.speaker.play_wav("./wav/mypleasure.wav")

	def _shutdown(self):
		print "Saying: E.V.E. will go to sleep now. Good bye!"
		self.speaker.play_wav("./wav/sleep.wav")
		sys.exit('+++++++++++++++++++++  E.V.E. HAS SHUTDOWN  ++++++++++++++++++++') 

################################################################################

	def listen(self):
		print "Saying: Yes?"
		self.speaker.play_wav("./wav/yes.wav")

		self.audioInput.listen()
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
			print "No connection."
			self.speaker.play_wav("./wav/internet_err.wav")
			return None

	def _parse_input(self, job):
		action_verb = "" 
		command_type = ""
		t_key = "" 
		i_key = ""
		preposition = ""
		query = ""

		words = job.recorded().split()

		for word in words:
			# set action verb if it comes before any other goalpost
			if word in ACTION_VERBS and action_verb == "" and t_key == "":
				action_verb = word 
			# set t_key if it comes before any other t_key
			elif word in T_KEYS and t_key == "":
				t_key = word
				command_type = word
			# set i_key if it comes before any other key
			elif word in I_KEYS and t_key == "" and i_key == "":
				i_key = word
				command_type = word
			# find prepositions in cases such as "youtube video of" or "google for"
			elif word in PREPOSITIONS and t_key != "":
				preposition = word
			# catch the stop recording case
			elif word == "no" and words[words.index(word) + 1] == "stop":
				print "Accidental recording"
				command_type = "no stop"
				break

		# get query if it exists
		if command_type not in I_KEYS and \
			command_type != "" and command_type != "no stop": 
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

		elif command_type == "youtube" or command_type == "video":
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
			self.voice_cmd.ai_respond(job, self.AI)

		# TODO refactor to conform to new standard
		elif job.recorded().find('change news source') != -1:
			self.voice_cmd.change_news_source(job)

		elif command_type == "news": 
			self.voice_cmd.get_news(job)

		elif command_type == "radio":
			self.voice_cmd.play_music(job)

		else:
			self.voice_cmd.ask_wolfram(job, self.AI)


		if not job.get_is_processed:
			self.speaker.say("Sorry, I didn't find any results.")


