from actions.actions_helper import ActionsHelper

class Webpage():
	"""
	processes requests for opening a specified webpage.
	"""

	def __init__(self, speaker):
		self.speaker = speaker

	def process(self, job, controller):
		phrase = job.recorded()[job.recorded().find(' ') + 1:]
		url = self._make_url(phrase)
		if url != "":
			self.speaker.say("opening " + url[12:])
			controller.open(url)
		else:
			self.speaker.say("sorry, I didn't find the web page.")

	def _make_url(self, phrase):
		# remove spaces in the phrase
		phrase = self._remove_spaces(phrase)

		# if phrase does not end with .com or other suffix append .com
		if phrase.find('.com') == -1 \
		and phrase.find('.edu') == -1 \
		and phrase.find('.org') == -1:
			phrase = phrase + ".com"

		# test website existence, return "" if website doesn't exist
		return ActionsHelper().test_url(phrase)

	def _remove_spaces(self, phrase):
		space = phrase.find(' ')
		while space != -1:
			phrase = phrase[:space] + phrase[space + 1:]
			space = phrase.find(' ')
		return "https://www." + phrase.lower()

	