#!/usr/bin/python
# -*- coding: utf-8 -*-

import aiml
import os.path
import marshal

def main():
	"""
	test program that tests the loading of the PyAIML AI,
	with and in the absence of the Memory.ses file.
	"""

	AI = aiml.Kernel()

	if os.path.isfile("standard.brn"):
	    AI.bootstrap(brainFile = "standard.brn")

	else:
		AI.learn("reduction0.safe.aiml")
		AI.learn("reduction1.safe.aiml")
		AI.learn("reduction2.safe.aiml")
		AI.learn("reduction3.safe.aiml")
		AI.learn("reduction4.safe.aiml")
		AI.learn("reductions-update.aiml")

		AI.learn("mp0.aiml")
		AI.learn("mp1.aiml")
		AI.learn("mp2.aiml")
		AI.learn("mp3.aiml")
		AI.learn("mp4.aiml")
		AI.learn("mp5.aiml")
		AI.learn("mp6.aiml")

		for subdir, dirs, files in os.walk('.'):
			 for file in files:
				if file[-4:] == 'aiml' and file.find('mp') == -1 \
								and file.find('reduction') == -1:
					AI.learn(file)

		AI.saveBrain("standard.brn")

	try:
		sessionFile = open("Memory.ses", "rb")
		session = marshal.load(sessionFile)
		sessionFile.close()
		for pred,value in session.items():
			AI.setPredicate(pred, value, "Memory")
	except Exception:
		AI._addSession("Memory") 

	# Loop forever, reading user input from the command
	# line and printing responses.
	x = 6
	while x > 0: 
		print AI.respond(raw_input("> "), "Memory")
		x = x - 1

	session = AI.getSessionData("Memory")
	sessionFile = open("Memory.ses", "wb")
	marshal.dump(session, sessionFile)
	sessionFile.close()
    
    
if __name__ == '__main__':
	main()
