import wolframalpha

class Wolfram:
	def __init__(self, tts, key):
		self.tts = tts
		self.key = key

	def process(self, job):
		if job.get_is_processed(): 
			return False

		if not self.key:
			self.tts.say("Please provide an API key to query the WolframAlpha database.")
			return False

		self.say(self.query(job.raw(), self.key))
		job.is_processed = True

	def query(self, phrase, key):
		return "hello" # substitute phrase