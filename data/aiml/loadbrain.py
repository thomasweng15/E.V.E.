#!/usr/bin/python
# -*- coding: utf-8 -*-

# load a new brain after updating aiml files.

import aiml
import os

CHATBOT_CONFIG = "./chatbot_config.txt"
AIML_SET = "./aiml_set/"

def main():
	AI = aiml.Kernel()
		
	AI.learn(AIML_SET + "reduction0.safe.aiml")
	AI.learn(AIML_SET + "reduction1.safe.aiml")
	AI.learn(AIML_SET + "reduction2.safe.aiml")
	AI.learn(AIML_SET + "reduction3.safe.aiml")
	AI.learn(AIML_SET + "reduction4.safe.aiml")
	AI.learn(AIML_SET + "reductions-update.aiml")

	AI.learn(AIML_SET + "mp0.aiml")
	AI.learn(AIML_SET + "mp1.aiml")
	AI.learn(AIML_SET + "mp2.aiml")
	AI.learn(AIML_SET + "mp3.aiml")
	AI.learn(AIML_SET + "mp4.aiml")
	AI.learn(AIML_SET + "mp5.aiml")
	AI.learn(AIML_SET + "mp6.aiml")

	for subdirs, dirs, files in os.walk(AIML_SET):
		for f in files:
			if f.find('aiml') != -1 or f.find('mp') != -1 or f.find('reduction') != -1:
				AI.learn(AIML_SET + f)


	AI.saveBrain("./standard.brn")

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
			AI.setBotPredicate(key_value[0], key_value[1].rstrip('\n'))

	# Loop forever, reading stdin and printing responses
	while 1: 
		print AI.respond(raw_input("> "))
    
if __name__ == '__main__':
	main()