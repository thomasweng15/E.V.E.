
import praw

class News():
	def __init__(self, speaker):
		self.speaker = speaker

	def process(self, job, controller):
		self.speaker.say("getting the world news.")
		r = praw.Reddit(user_agent='evebot v1.0 by /u/tw334')
		submissions = r.get_subreddit('worldnews').get_new(limit=10)
		# TODO make titles spoken
		for submission in submissions:
			print ">>> " + submission.title