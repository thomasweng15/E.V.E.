#!/usr/bin/python
# -*- coding: utf-8 -*-

from voicecmd import VoiceCommand
from inputs.microphone import Microphone
from ex.exception import NotUnderstoodException

import tts
import stt
import sys
import urllib2
import aiml # AI
import marshal # for AI persistence


class Job:
	def __init__(self, recorded_text):
		self.recorded_text = recorded_text
		self.is_processed = False

	def get_is_processed(self):
		return self.is_processed

	def recorded(self):
		return self.recorded_text


class Brain:
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
		except Exception:
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
		except Exception as err: pass
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
			first_word, second_word = self._get_first_two_words(job.recorded())
			self._execute_voice_cmd(job, first_word, second_word)

	def _set_job(self):
		try:
			speech_to_text = stt.Google(self.audioInput)
			recorded_text = speech_to_text.get_text()
			return Job(recorded_text)
		except NotUnderstoodException:
			print "Sorry, I didn't get that."
			self.speaker.play_wav("./wav/didntget.wav")
			return None

	def _get_first_two_words(self, recorded_text):
		first_word = (recorded_text.split(' ')[0]).lower() 
		if recorded_text.find(' ') >= 1:
			second_word = (recorded_text.split(' ')[1]).lower()
		else:
			second_word = ""
		return first_word, second_word

	def _execute_voice_cmd(self, job, first_word, second_word):
		if first_word == "no" or job.recorded().find('no stop') != -1:
			self.voice_cmd.accidental_recording()
		
		elif first_word == "open":
			if second_word != "": # open webpage
				self.voice_cmd.open_webpage(job)
			else:
				self.speaker.say("no webpage specified.")
		
		elif first_word == "google" or first_word == "search":
			if second_word != "": # pull up query results
				self.voice_cmd.google(job)
			else: 
				self.speaker.say("no query provided.")
		
		elif first_word == "youtube":
			if second_word != "":
				if second_word == "search": # return youtube results
					self.voice_cmd.search_youtube(job)
				else: 
					self.voice_cmd.play_youtube(job)
			else:
				self.speaker.say("no query provided.")
		
		elif job.recorded().lower().find('screenshot') != -1: # take screenshot
			self.voice_cmd.take_screenshot()
		
		elif first_word == "computer": # AI responds
			self.voice_cmd.ai_respond(job, self.AI, "Memory")
		
		elif job.recorded().find('news') != -1: # get news
			self.voice_cmd.get_news(job)
		
		#elif first_word == "play":
		#	self.voice_cmd.play_music(job)
		
		else:
			self.voice_cmd.ask_wolfram(job)


		if not job.get_is_processed:
			self.speaker.say("Sorry, I didn't find any results.")












