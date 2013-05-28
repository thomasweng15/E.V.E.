E.V.E.
======

Description
-----------
EVE is a Star Trek / Jarvis type computer.
EVE will receive vocal or textual queries and return relevant web results accompanied by voice.

Originally based on a similar project by Rob McCann, where the computer would both receive and return audio, with no text.

Dependencies
------------
*	julius
*	python: pyaudio
*	python: requests
*	python: pydub
*	python: pyAIML
* 	python: praw
*	Internet connection and web browser
*	Wolfram Alpha API key
*	a microphone

Installation
------------
1. 	Install the necessary dependencies on your computer.
2. 	Clone this project.
3. 	Run the project by running "python eve.py" in the terminal in the EVE directory:
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
2. 	make EVE cross-platform.
3. 	design alarm clock
4. 	improve aiml brain / implement sessions and setting predicates
		have cmdline option to wipe session
5. 	change news to a better source than reddit

Other Notes
-----------
grooveshark page alternatives:
The tinysong grooveshark api:
http://tinysong.com/api#/result/martin solveig/
mopidy is another possible alternative.
or spotify: https://developer.spotify.com/technologies/web-api/search/

consider switching to true knowledge from wolfram alpha