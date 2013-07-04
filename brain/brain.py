from voicecmd import VoiceCommand
from inputs.microphone import Microphone
from ex.exception import NotUnderstoodException
from ex.exception import ConnectionLostException

import tts
import stt
import sys
import subprocess

# natural voice command parsing keywords
T_KEYS = ['google', 'youtube', 'search', 'open', 'computer', 'radio', 'video']
I_KEYS = ['news','screenshot']
ACTION_VERBS = ['search', 'look', 'pull', 'get', 'give']
PREPOSITIONS = ['for', 'on', 'of']


class Job:
	"""
	Store text converted from recorded voice input, 
	and a boolean describing the job's state of whether 
	or not it has been processed. Job instances are 
	processed through the VoiceCommand class.
	
	"""
	def __init__(self, recorded_text):
		self.recorded_text = recorded_text
		self.query = ""
		self.is_processed = False

	def get_is_processed(self):
		""" 
		Return whether the job has been processed 
		through the VoiceCommand process or not.
		
		"""
		return self.is_processed

	def recorded(self):
		"""
		Return the text version of audio input 
		interpreted by the Google text to speech engine.

		"""
		return self.recorded_text

	def set_query(self, query):
		"""
		Set the query of the job, extracted from recorded text 
		by Brain.classify_job(). 

		"""
		self.query = query

	def query(self):
		"""Return the query associated with the job."""
		return self.query


class Brain:
	"""
	Initialize everything EVE needs to function, 
	listen for activation input from julius, 
	and execute commands based on voice input.
	The Brain class coordinates all other components
	of EVE.
	
	"""
	def __init__(self):
		self.audioInput = Microphone()
		self.speaker = tts.Google()
		self.voice_cmd = VoiceCommand(self.speaker)
		self.print_welcome()

		print "Saying: Hello there!"
		self.speaker.play_wav("./wav/hello.wav")

	def print_welcome(self):
		"""
		Print welcome message in terminal when E.V.E. first starts up
		and initializes the Brain class.
		
		"""
		welcome_message =  """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++  Welcome to E.V.E.  ++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                                                              +
+                 Say 'okay computer' to start!                +
+                                                              +
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	"""
		print welcome_message

################################################################################


	def process_input(self, ln, julius_proc):
		"""
		Take input text and extract activation commands
		from it if they exist. If using julius to get voice input, 
		the grammar file used by julius error free.
		
		"""
		startstring = 'sentence1: <s> '
		endstring = ' </s>'

		line = ln.lower()
		if not line:
			return False

		if 'missing phones' in line:
			sys.exit('Error: Missing phonemes for the used grammar file.')

		if line.startswith(startstring) and line.strip().endswith(endstring):
			phrase = line.strip('\n')[len(startstring):-len(endstring)]
			return self.parse(phrase, julius_proc)

	def parse(self, phrase, julius_proc):
		"""
		Identify activation commands from input 
		extracted by the 'process_input' function and
		call the appropriate function for a given command.
		
		"""
		params = phrase.split()
		if params == ['okaycomputer']:
			if julius_proc is not None:
				julius_proc.kill()
			self.okaycomputer()

		elif params == ['computer', 'lets', 'talk']:
			if julius_proc is not None:
				julius_proc.kill()
			self.conversation()
		
		elif params == ['thanks', 'darling']:
			if julius_proc is not None:
				julius_proc.kill()
			self.accept_thanks()

		elif params == ['computer', 'power', 'down']:
			if julius_proc is not None:
				julius_proc.kill()
			self.shutdown()
		else: 
			return False

		return True

	def okaycomputer(self):
		"""
		Start recording and listening for a voice command
		if internet connection is available.

		"""
		print "Activating..."
		# ensure that internet connection is available
		if not self.speaker.say("Yes?"): 
			return 
		conversation_mode = False
		self.listen(conversation_mode)

	def conversation(self):
		"""Start a conversation with E.V.E."""
		print "Activating..."
		# ensure that internet connection is available
		if not self.speaker.say("Okay, what do you want to talk about?"):
			return
		conversation_mode = True 
		while 1:
			self.listen(conversation_mode) # True for conversation mode

	def accept_thanks(self):
		"""Reply to user's gratitude."""
		print "Saying: My pleasure."
		self.speaker.play_wav("./wav/mypleasure.wav")

	def shutdown(self):
		"""Close the E.V.E. program."""
		print "Saying: E.V.E. will go to sleep now. Good bye!"
		self.speaker.play_wav("./wav/sleep.wav")
		sys.exit('+++++++++++++++++++++  E.V.E. HAS SHUTDOWN  ++++++++++++++++++++') 

################################################################################

	def listen(self, conversation):
		"""Initiate listening for voice commands."""
		self.audioInput.listen()
		job = self.set_job()
		
		if job is None:
			return

		if conversation is False:
			self.classify_job(job)
		else: 
			self.execute_voice_cmd(job, "computer", job.query)

	def set_job(self):
		"""
		Send audio input to Google's Speech to text
		engine to be interpreted, and then init a Job class 
		with the returned text if successful. 

		"""
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

	def classify_job(self, job):
		"""
		Match keywords and keyword order with 
		words in the job to classify which voice command 
		the job requires.

		"""
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
		
		self.execute_voice_cmd(job, command_type, query)

	def execute_voice_cmd(self, job, command_type, query):
		"""
		Execute the method in the VoiceCommand class 
		that is associated with the classified command type.

		"""
		if command_type == "no stop":
			self.voice_cmd.accidental_recording()

		elif command_type == "open":
			if query != "":
				self.voice_cmd.open_webpage(job)
			else:
				self.speaker.say("no webpage specified.")

		elif command_type == "google" or command_type == "search":
			if query != "":
				self.voice_cmd.search(job)
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
			self.voice_cmd.chatbot_respond(job)

		elif command_type == "news": 
			self.voice_cmd.get_news(job)

		elif command_type == "radio":
			self.voice_cmd.play_music(job)

		else:
			self.voice_cmd.ask_wolfram(job)


		if not job.get_is_processed:
			self.speaker.say("Sorry, I didn't find any results.")


