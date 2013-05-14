Jarvis
=====

Description
-----------

The beginnings of a Jarvis computer.
Jarvis will receive vocal or textual queries and return relevant web results accompanied by voice.

Based on Pi-Voice by Rob McCann.

Currently records voice, parses first two words (if they exist) into text, and then responds before opening a webpage.

Dependencies
------------
urllib
pyaudio
requests
pydub
Internet connection and firefox

Installation
------------
instructions under construction!

Next Steps
----------
1.	implement commands beyond opening certain webpages (e.g. search)
2.	catch exceptions such as no internet connection
3.	suppress ALSA errors

Other Details
-------------
* Jarvis should be able to execute a set of commands, 
 e.g. search, open, youtube. 
* Jarvis should handle errors with interpretation and ask for reiteration. 
* It would be nice if Jarvis could listen for the end of a query, 
but if not, Jarvis should be able to listen for as long as a button is pressed or at least for a specified amount of time.

Notes
-----
julius -quiet -input mic -C julian.jconf 2>/dev/null | ./command.py

http://bloc.eurion.net/archives/2008/writing-a-command-and-control-application-with-voice-recognition/
firefox -new-tab <url>
	youtube.com
	google.com
	facebook.com

use grooveshark for music playing 
http://grooveshark.com/#!/search?q=that+girl+justin+timberlake
or the tinysong grooveshark api:
http://tinysong.com/api#/result/martin solveig/
mopidy is a possible alternative.

http://www.voxforge.org/home/docs/faq/faq/what-is-a-dialog-manager

http://www.youtube.com/results?search_query=frank+ocean&page=&utm_source=opensearch

google custom search api
https://www.googleapis.com/customsearch/v1?parameters

