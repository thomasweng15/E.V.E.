#!/usr/bin/python
# -*- coding: utf-8 -*-

import tospeech
from inputs.microphone import Microphone

def main():
	
	#while loop to listen for queries?
	audioInput = Microphone()
	audioInput.listen()

	# text to speech test text
	#speaker = tts.Google()
	#testtext = "Hello! my name is Jarvis and I am a talking computer."
	#speaker.say(testtext)

if __name__ == "__main__":
	main()

	
#def listen():
	#audioInput() = Microphone
	#audioInput.listen()
	



