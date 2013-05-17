HAL-E
======

Description
-----------

The beginnings of a 'Jarvis' computer.
HAL-E will receive vocal or textual queries and return relevant web results accompanied by voice.

Originally based on a similar project by Rob McCann, where the computer would both receive and return audio, with no text.

Currently records voice, parses words into text, and then responds before executing a command such as pulling up a list of youtube searches.

I am working on this project using Ubuntu 13.04. This project may not work for non linux operating systems.

Dependencies
------------
*	julius and julius-voxforge
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
3. 	Run the project by running "sh start.sh" in the terminal in the Jarvis directory:
		The program will listen for the phrase "OK JARVIS."
		The program will then listen for a command, e.g
			"open google.com"
			"youtube search man of steel"
		After executing the command, Jarvis will again listen for "OK JARVIS."

Available Commands
------------------
*	'open WEBSITE'  -- open a website in your default browser.
*	'google QUERY'	-- pull up a list of search results.
*	'youtube [search] QUERY'	-- play the first youtube video (by relevance) returned by the query. If [search] is specified, pull up a list of youtube results instead. 
*	'grooveshark/play QUERY' 	-- pull up grooveshark search results.
*	'screenshot'	-- if 'screenshot' appears in the recording after checking the above options, take a screenshot and save it in the Jarvis directory.
*	'[wolfram]'	-- if 'wolfram' is the first word of a general query, pull up the wolfram alpha query result. Otherwise, Jarvis will just read back the result of the query, unless it is an image (in which case it will pull up the query result in the browser.)

Next Steps
----------
1.  make more julius commands
2. 	come up with a better way to manage music.
3. 	add screenrecord capability
4. 	design a gui for hal-e
5. 	make Jarvis capable of reading out the weather instead of displaying a web page

Other Notes
-----------
grooveshark page alternatives:
The tinysong grooveshark api:
http://tinysong.com/api#/result/martin solveig/
mopidy is another possible alternative.

consider switching to true knowledge from wolfram alpha
consider using espeak http://espeak.sourceforge.net/

is there a way to have the job of saying a response and bringing up a webpage be in parallel?

