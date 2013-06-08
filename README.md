E.V.E.
======

Description
-----------
E.V.E. is a Star Trek / Jarvis type computer. Run the program, and E.V.E. will activate whenever you say "okay computer," after which you can ask it a question / command. 

E.V.E. accepts many different types of questions and commands, such as "What was the temperature in London on the 13th July 1982?", "Youtube the Star Trek Into Darkness trailer," and "Eve, what sports do you like to play?" See 'Usage' for a full list of what E.V.E. can do.

This project was cloned from a [similar project](https://github.com/rob-mccann/Pi-Voice) by Rob McCann. I have implemented some of the next steps listed in that project here, and will be contributing back to that project in the next few days. Yay open source!

The project is developed for Linux, but has the potential to be multi-platform. Perhaps you can help!


Dependencies
------------
*	julius and julius-voxforge packages
*	ffmpeg package
*	python: pyaudio
*	python: requests
*	python: pydub
*	python: PyAIML
* 	python: praw
* 	python: gmusicapi
* 	python: wolframalpha

Other requirements:
*	Wolfram Alpha API key
*	Internet connection and web browser
*	A microphone

See 'Installation' for detailed installation instructions.


Usage
-----
Run the project by entering 'python eve.py' into the terminal in the EVE directory.
E.V.E. will start up and then listen for a spoken activation command (e.g. 'Okay Computer'). 

Note: You may find several lines of ALSA error messages after starting up eve.py. If the error messages do not terminate the program and return to the terminal prompt, then EVE can accept commands and function normally. The errors do not affect the running of the program, and I am working on removing the messages. 

### Activation Commands:
processed by Julius Speech Recognition Software.

*	"Okay Computer" 			-- E.V.E. will listen for a voice command, 
								which is described in further detail below. 
								After executing the command, E.V.E. will 
								listen for another activation command. 

*	"Computer Power Down" 		-- E.V.E. will shut down.

*	"Thanks Darling" 			-- E.V.E. will accept the thanks and listen for another 
								activation command.

### Voice Commands:
processed by the google text-to-speech engine.

*	"open [webpage]" 			-- opens specified webpage.

*	"google/search [query]"		-- googles specified query.

*	"youtube [query]			-- plays first youtube video returned by query.

*	"youtube search [query]"	-- returns list of videos found by query.

*	"news"						-- returns ten newest worldnews items from reddit

*	"screenshot"				-- takes a screenshot

*	"Computer, [query]"			-- AI responds to query

*	"[query]"					-- runs query against wolfram alpha

*	"no/no stop"				-- accidental recording; do nothing.


Installation 
------------
These installation instructions work for Ubuntu Linux.

### Installing julius and julius voxforge:
	'sudo apt-get install julius'
	'sudo apt-get install julius-voxforge'

### Installing ffmpeg (for pydub):
	'sudo apt-get install ffmpeg'

### Installing python packages using pip:
	'pip install pyaudio'
	'pip install requests'
	'pip install praw'
	'pip install wolframalpha'
	'pip install pydub'
	'pip install pyaiml'

### Getting a Wolfram Alpha API Key:
	1. Sign up for a wolfram alpha account 
		--'https://developer.wolframalpha.com/portal/apisignup.html'
	2. Request an API key
	3. In the terminal, 'export WOLFRAM_API_KEY='AAAAAA-AAAAAAAAAA''

### Installing E.V.E.:
	'git clone https://github.com/thomasweng15/E.V.E..git'

Installation complete! Take a look at "Usage" to run the program!


Next Steps
----------
1. 	use unofficial google music api to manage music
2. 	come up with a better way to present the news.
3. 	design a GUI! 


Contributors
------------
Thomas Weng

Rob McCann