from actions.actions_helper import ActionsHelper
import sys

DATAFILE = "./data/user_config.txt"


class News():
	"""
	Process jobs requesting the news.
	
	"""
	def __init__(self, speaker):
		self.speaker = speaker
		self.get_news_url()
		
	def get_news_url(self):
		"""Find news url from datafile."""
		try:
			f = open(DATAFILE, 'r')
		except IOError:
			self.speaker.say("Error, datafile cannot be found.")
			sys.exit(1)

		found_news_url = False
		for line in f:
			if line.find("news_url::") != -1:
				self.news_url = line[10:]
				found_news_url = True
				break

		if found_news_url != True:
			self.speaker.say("Oops, datafile does not contain news URL item.")
		f.close()

	def process(self, job, controller):
		"""Process News job request."""
		self.speaker.say("getting the news.")
		controller.open(self.news_url)

	def update_news_url(self):
		"""Update the news url in the datafile."""
		self.speaker.say("Please enter a new news URL.")
		url = raw_input("Enter the exact url of a news website: ")
		if ActionsHelper().test_url(url) != "":
			f = open(DATAFILE, 'r')
			output = []
			updated = False
			for line in f:
				if line.find('news_url::') == -1:
					output.append(line)
				else:
					news_line = "news_url::" + url
					output.append(news_line)
					self.news_url = url
					self.speaker.say("Successfully updated news source.")
					updated = True
			f.close()

			if updated != True:
				self.speaker.say("Oops, news source update failed.")
				print "Error: update to news source failed."

			f_out = open(DATAFILE, 'w')
			f_out.writelines(output)
			f_out.close()
		else: 
			# TODO make url handling more robust and comprehensive
			self.speaker.say("Error: submitted URL is invalid.")

	