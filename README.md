E.V.E.
======

Description
-----------
E.V.E. is a Star Trek / Jarvis type computer, designed to receive vocal queries or commands and then respond or execute them appropriately. See 'Usage' for details.

Cloned from a similar project by Rob McCann, where the objective was for the program to only respond aurally to voice input.

The program is designed for Linux, but has the potential to be cross-platform. Perhaps you can help!

Dependencies
------------
*	julius and julius-voxforge packages
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
1. 	Register with Wolfram Alpha and get an API key.
2. 	Add the API key to your PATH by entering in the command line:
		export WOLFRAM_API_KEY='AAAAAA-AAAAAAAAAA'
3. 	Install the necessary dependencies on your computer.
2. 	Clone this project.	

Usage
-----
Run the project by entering "python eve.py" into the terminal in the EVE directory.
E.V.E. will start up and then listen for a spoken activation command. 

Activation Commands:
  processed by Julius Speech Recognition Software.

*	"Okay Computer" 			-- E.V.E. will listen for a voice command, 
								which is described in further detail below. 
								After executing the command, E.V.E. will 
								listen for another activation command. 

*	"Shut Down Program" 		-- E.V.E. will shut down.

*	"Thanks Darling" 			-- E.V.E. will accept the thanks and listen for another 							   	activation command.

Voice Commands:
  processed by the google text-to-speech engine.

*	"open [webpage]" 			-- opens specified webpage.
*	"google/lookup [query]"		-- googles specified query.
*	"youtube [query]			-- plays first youtube video returned by query.
*	"youtube search [query]"	-- returns list of videos found by query.
*	"grooveshark/play [query]"	-- look up query on grooveshark.
*	"news"						-- returns ten newest worldnews items from reddit
*	"screenshot"				-- takes a screenshot
*	"check [query]"				-- runs query against wolfram alpha
*	"[query]"					-- AI responds to query
*	"no/no stop"				-- accidental recording; do nothing.


Next Steps
----------
1. 	come up with a better way to manage music.
2. 	make EVE cross-platform.
5. 	change news to a better source than reddit
6. 	make a cmdline option to delete an AI session and "erase memory"

Contributors
------------
Thomas Weng