import aiml

BRAINFILE = "./data/standard.brn"
CHATBOT_CONFIG = "./data/chatbot_config.txt"

class Chatbot():
	"""
	Process requests to converse with the chatbot.

	"""
	def __init__(self, speaker):
		self.chatbot = aiml.Kernel()
		self.chatbot.bootstrap(brainFile=BRAINFILE)
		self.speaker = speaker
		self.configure_predicates()

	def configure_predicates(self):
		"""Load bot predicates from brainfile."""
		try: 
			f = open(CHATBOT_CONFIG)
		except IOError:
			self.speaker.say("Error: chatbot configuration file not found.")
			sys.exit(1)

		bot_predicates = f.readlines()
		f.close()
		for bot_predicate in bot_predicates:
			key_value = bot_predicate.split('::')
			if len(key_value) == 2:
				self.chatbot.setBotPredicate(key_value[0], key_value[1].rstrip('\n'))

	def process(self, job):
		"""Process chat bot job requests."""
		if job.query != "":
			response = self.chatbot.respond(job.query)
		else:
			response = self.chatbot.respond(job.recorded())
		self.speaker.say(response)

		job.is_processed = True