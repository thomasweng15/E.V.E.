Jarvis
======

Description
-----------

The beginnings of a Jarvis computer.
Jarvis will receive vocal or textual queries and return relevant web results accompanied by voice.

Originally based on a similar project by Rob McCann, where the computer would both receive and return audio, with no text.

Currently records voice, parses words into text, and then responds before executing a command such as pulling up a list of youtube searches.

I am working on this project using Ubuntu 13.04. This project may not work for non linux operating systems.

Dependencies
------------
*	pyaudio
*	requests
*	pydub
*	Internet connection and web browser
*	Wolfram Alpha API key
*	a microphone

Installation
------------
1. 	Install the necessary dependencies on your computer.
2. 	Clone this project.
3. 	Run the project by running "sh start.sh" in the terminal:
		The program will listen for the phrase "OK JARVIS COMPUTER."
		The program will then listen for a command, e.g
			"open google.com"
			"youtube search man of steel"
		After executing the command, Jarvis will again listen for "OK JARVIS COMPUTER."

Next Steps
----------
1. 	make sure julius does not reopen recording immediately after executing a command
	and see if julius can respond to somthing shorter than OK JARVIS COMPUTER
2. 	instead of pulling up a page of music results, automatically play first search result.
3. 	add screenshot and screenrecord capabilities
4. 	design a gui for jarvis 
5. 	make internet connection loss error more robust -- detect connection errors mid program

Other Notes
-----------
grooveshark page alternatives:
The tinysong grooveshark api:
http://tinysong.com/api#/result/martin solveig/
mopidy is another possible alternative.

consider switching to true knowledge from wolfram alpha
consider using festival / espeak

is there a way to have the job of saying a response and bringing up a webpage be in parallel?

