Jarvis
=====

The beginnings of a Jarvis computer.
Jarvis will receive vocal or textual queries and return relevant web results accompanied by voice.

Based on Pi-Voice by Rob McCann.

Currently able to record audio, parse audio into text using Google STT, and speak using Google TTS.

Dependencies:
pyaudio
requests
pydub

Next Steps:
1. implement command parsing
2. catch exceptions such as no internet connection

Other Details:
-Jarvis should be able to execute a set of commands, 
 e.g. search, open, youtube. 
-Jarvis should handle errors with interpretation and ask for reiteration. 
-It would be nice if Jarvis could listen for the end of a query, 
but if not, Jarvis should be able to listen for as long as a button is pressed or at least for a specified amount of time.

Notes:
julius -quiet -input mic -C julian.jconf 2>/dev/null | ./command.py

http://bloc.eurion.net/archives/2008/writing-a-command-and-control-application-with-voice-recognition/
firefox -new-tab <url>
	youtube.com
	google.com
	facebook.com

use grooveshark for music playing 
http://grooveshark.com/#!/search?q=that+girl+justin+timberlake
mopidy is a possible alternative.

http://www.voxforge.org/home/docs/faq/faq/what-is-a-dialog-manager