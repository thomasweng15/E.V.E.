from actions.actions_helper import ActionsHelper


class News():
	"""
	processes jobs requesting the news.
	"""

	def __init__(self, speaker):
		self.speaker = speaker
		# get news url from datafile
		# TODO catch exception when datafile cannot be found
		f = open('./actions/datafile.txt', 'r')
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
		self.speaker.say("getting the news.")
		controller.open(self.news_url)

	def set_news_url(self):
		self.speaker.say("Please enter a new news URL.")
		url = raw_input("Enter the exact url of a news website: ")
		if ActionsHelper().test_url(url) != "":
			# update news url in datafile
			f = open('./actions/datafile.txt', 'r')
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

			f_out = open('./actions/datafile.txt', 'w')
			f_out.writelines(output)
			f_out.close()
		else: 
			# TODO make url handling more robust and comprehensive
			self.speaker.say("Error: submitted URL is invalid.")
			print "Error: submitted url is invalid."

	