E.V.E.
======

Description
-----------
E.V.E. is a Star Trek / Jarvis type computer. Run the program, and E.V.E. will activate whenever you say "okay computer," after which you can ask it a question / command. 

E.V.E. accepts many different types of questions and commands, such as "What was the temperature in London on the 13th July 1982?", "Get me a YouTube video of the Star Trek Into Darkness trailer," and "Computer, what sports do you like to play?" 

As the example cases demonstrate, E.V.E. now understands voice commands given in natural conversational language (e.g. "could you help me Google Seattle, Washington?", "pull up a search on youtube for cute cats"). See 'Usage' for a full list of what E.V.E. can do.

This project was cloned from a [similar project](https://github.com/rob-mccann/Pi-Voice) by Rob McCann. I have implemented some of the next steps listed in that project here, and will be contributing back to that project. Yay open source!

The project is developed for Linux, but has the potential to be multi-platform. Perhaps you can help!


Dependencies
------------
*	julius and julius-voxforge packages
*	ffmpeg package
*	python: pyaudio
*	python: requests
*	python: pydub
*	python: PyAIML
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

#### "Okay Computer" 
E.V.E. will listen for a voice command, which is described in further detail below. After executing the command, E.V.E. will listen for another activation command.

#### "Computer Power Down" 		
E.V.E. will shut down.

#### "Thanks Darling" 		
E.V.E. will accept the thanks and listen for another activation command.



### Voice Commands:
processed by the google text-to-speech engine.

As mentioned above, the program is able to understand more naturally structured queries than the ones listed below. This feature is still experimental, but for the most part you can utter commands in conversational language:
	'find me a youtube video of Rick Astley'
	'I need some study music, please play the Beatles'
One restriction that still exists is that you should not say anything conversational or extraneous at the end of your input, as that will become appended to your query.

#### "open [webpage]" 
opens specified webpage.

#### "google/search [query]"
googles specified query.

#### "youtube [query]"
plays first youtube video returned by query.

#### "youtube search [query]"
returns list of videos found by query.

#### "Computer, [query]"
Conversational AI responds to query

#### "[query]"
runs query against wolfram alpha. If wolfram does not find a response, the conversational AI will respond. As a result, you can ask conversational questions such as "do you like sports?" directly as a voice command, without needing to prefix it with 'computer'.

#### "play [artist]"
opens Last.fm radio to play similar artists. (Current music streaming solutions all require premium accounts. Last.fm radio doesn't even require user authentication)

#### "...no stop..."
accidental recording; do nothing.

#### "..screenshot..."
takes a screenshot

#### "...news..."
opens a news website of your choosing (default is currently set to Bing News as I personally think the layout is really good. But you can change it to whatever you want!)

#### "change news source"
this command takes precedence over the one above. The program will prompt you for a new news url.



Installation 
------------
These installation instructions work for Ubuntu Linux.

#### Install building tool chain:
`$ sudo apt-get install build-essential`

#### Install julius and julius voxforge:
`$ sudo apt-get install julius julius-voxforge`

#### Download and install portaudio
[from here](http://www.portaudio.com/download.html)

#### Install ffmpeg (for pydub):
`$ sudo apt-get install ffmpeg`

#### Install python packages using pip:
`$ pip install -r requirements.txt`

#### Install pyaiml
	$ git clone git://pyaiml.git.sourceforge.net/gitroot/pyaiml/pyaiml
	$ python setup.py install

#### Getting a Wolfram Alpha API Key(AppID):
1. [Sign up for a wolfram alpha account](https://developer.wolframalpha.com/portal/apisignup.html)
2. Request an API key(AppID)
3. In the terminal, 'export WOLFRAM_API_KEY='AAAAAA-AAAAAAAAAA''

#### Run E.V.E.:
	$ git clone https://github.com/thomasweng15/E.V.E..git
	$ python eve.py

#### Other Setup:
	Ensure that your microphone is set up and that the input volume 
	is not too low or too high. You can check this using the "Sound" 
	utility in your settings menu under the "Input" tab.

Installation complete! Take a look at "Usage" to run the program!


Next Steps
----------
1. 	make screenshot storage location variable and store the path in datafile.txt.
2.  provide Arduino communication/control as an action to be triggered by voice command.
3. 	design a GUI! 
4.	when no results are found by wolfram alpha, redirect to AI response
5.  Add a mute function


Contributors
------------
*	Thomas Weng
*	Tevin Zhang
*	Rob McCann
            