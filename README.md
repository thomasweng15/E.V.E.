Jarvis
=====

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
*	Internet connection and firefox
*	Wolfram Alpha API key

Installation
------------
1. 	Install the necessary dependencies on your computer.
2. 	Clone this project.
3. 	Run the project by running jarvis.py.

Next Steps
----------
1. 	use julius to be always listening for "Jarvis"
2. 	incorporate music api

Other Notes
-----------
julius -quiet -input mic -C julian.jconf 2>/dev/null | ./command.py

julius example:
http://bloc.eurion.net/archives/2008/writing-a-command-and-control-application-with-voice-recognition/

grooveshark page alternatives:
The tinysong grooveshark api:
http://tinysong.com/api#/result/martin solveig/
mopidy is another possible alternative.

General resource:
http://www.voxforge.org/home/docs/faq/faq/what-is-a-dialog-manager

consider switching to true knowledge from wolfram alpha

