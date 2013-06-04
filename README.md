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
*	python: pyaudio
*	python: requests
*	python: pydub
*	python: PyAIML
* 	python: praw
* 	python: wolframalpha

Other requirements:
*	Wolfram Alpha API key
*	Internet connection and web browser
*	A microphone

See 'Installation' for detailed installation instructions.


Usage
-----
Run the project by entering 'python eve.py' into the terminal in the EVE directory.
E.V.E. will start up and then listen for a spoken activation command. 

### Activation Commands:
processed by Julius Speech Recognition Software.

*	"Okay Computer" 			-- E.V.E. will listen for a voice command, 
								which is described in further detail below. 
								After executing the command, E.V.E. will 
								listen for another activation command. 

*	"Computer Power Down" 		-- E.V.E. will shut down.

*	"Thanks Darling" 			-- E.V.E. will accept the thanks and listen for another 							   	activation command.

### Voice Commands:
processed by the google text-to-speech engine.

*	"open [webpage]" 			-- opens specified webpage.

*	"google/search [query]"		-- googles specified query.

*	"youtube [query]			-- plays first youtube video returned by query.

*	"youtube search [query]"	-- returns list of videos found by query.

*	"grooveshark/play [query]"	-- look up query on grooveshark.

*	"news"						-- returns ten newest worldnews items from reddit

*	"screenshot"				-- takes a screenshot

*	"Eve [query]"				-- AI responds to query

*	"[query]"					-- runs query against wolfram alpha

*	"no/no stop"				-- accidental recording; do nothing.


Installation 
------------
These installation instructions work for Ubuntu Linux.

### Installing julius and julius voxforge:
	'sudo apt-get install julius'
	'sudo apt-get install julius-voxforge'

### Installing pyaudio:
	Download from website 'http://people.csail.mit.edu/hubert/pyaudio/'
	'dpkg -i python{,3}-pyaudio_0.2.7-1_{i386,amd64}.deb'

### Installing requests:
	'pip install requests==0.14.2'

### Installing praw:
	'pip install praw'

### Installing wolframalpha:
	'pip install wolframalpha'

### Installing pydub:
	'pip install pydub'

### Installing PyAIML:
	'wget http://sourceforge.net/projects/pyaiml/files/PyAIML%20%28unstable%29/0.8.6/PyAIML-0.8.6.tar.gz/'
	'tar xzvf PyAIML-0.8.6.tar.gz'
	'cd PyAIML-0.8.6/'
	'sudo python setup.py install'

### Getting a Wolfram Alpha API Key:
	Sign up for a wolfram alpha account 
		--'https://developer.wolframalpha.com/portal/apisignup.html'
	Request an API key
	In the terminal, 'export WOLFRAM_API_KEY='AAAAAA-AAAAAAAAAA''

### Installing E.V.E.:
	'git clone https://github.com/thomasweng15/E.V.E..git'


Next Steps
----------
1. 	come up with a better way to manage music.
2. 	come up with a better way to present the news.


Contributors
------------
Thomas Weng

Rob McCann