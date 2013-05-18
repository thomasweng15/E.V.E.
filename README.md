E.V.E.
======

Description
-----------
Acronym: E.V.E. Voice-activated 'E'-ssistant (yes, it's really corny.)
A Star Trek / Jarvis type computer.
EVE will receive vocal or textual queries and return relevant web results accompanied by voice.

Originally based on a similar project by Rob McCann, where the computer would both receive and return audio, with no text.

Currently records voice, parses words into text, and then responds before executing a command such as pulling up a list of youtube searches.

I am working on this project using Ubuntu 13.04. This project may not work for non linux operating systems.

Dependencies
------------
*	julius
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
3. 	Run the project by running "sh start.sh" in the terminal in the EVE directory:
		The program will listen for the activation command "okay computer."
		The program will then listen for a voice command, e.g
			"open google.com"
			"youtube search man of steel"
		After executing the command, EVE will again listen for the activation command
		until it hears 'shut down program.'

Available Commands
------------------
After speaking the activation command these commands are available:
*	'open WEBSITE'  
	-- open a website in your default browser.
*	'google QUERY'	
	-- pull up a list of search results.
*	'youtube [search] QUERY'	
	-- play the first youtube video (by relevance) returned by the query. If [search] is specified, pull up a list of youtube results instead. 
*	'grooveshark/play QUERY' 	
	-- pull up grooveshark search results.
*	'wolfram QUERY'	
	-- pull up the wolfram alpha result for the query.
*	'screenshot'	
	-- if 'screenshot' appears in the recording after checking the above options, take a screenshot and save it in the EVE directory.
*	'QUERY'	
	-- general queries are sent to wolfram alpha for an answer.
*	'Shutdown Program' 	
	-- terminates the program.

Next Steps
----------
1. 	come up with a better way to manage music.
2. 	design a gui for eve (wxPython?)
3. 	make EVE capable of reading text in general?

Other Notes
-----------
grooveshark page alternatives:
The tinysong grooveshark api:
http://tinysong.com/api#/result/martin solveig/
mopidy is another possible alternative.
or spotify: https://developer.spotify.com/technologies/web-api/search/

consider switching to true knowledge from wolfram alpha

espeak http://espeak.sourceforge.net/ has lower quality tts than google but does not require an internet connection...

is there a way to have the job of saying a response and bringing up a webpage be in parallel?

overlaying wav files