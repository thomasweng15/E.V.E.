#!/usr/bin/python
# -*- coding: utf-8 -*-

import audiotools
import wave
import pyaudio
import tempfile
import requests
from pydub import AudioSegment
import os

def main():
	# text to speech test text
	testtext = "Hello! my name is Jarvis and I am a talking computer."
	say(testtext)


# make Jarvis say the words in text
def say(text):
	print "Saying: " + text

	# add turn all spaces into pluses
	text = spacestoPluses(text)

	# query google text to speech 
	# store result in temp mp3
	(_,tts_mp3_filename) = tempfile.mkstemp('.mp3')
	request_url = "http://translate.google.com/translate_tts?ie=utf-8&tl=en&q=" + text
	r = requests.get(request_url)
	f = open(tts_mp3_filename, 'wb')
	f.write(r.content) 
	f.close()

	# convert mp3 file into wav using pydub
	(_,tts_wav_filename) = tempfile.mkstemp('.wav')
	sound = AudioSegment.from_mp3(tts_mp3_filename)
	sound.export(tts_wav_filename, format="wav")

	play_wav(tts_wav_filename)

	os.remove(tts_mp3_filename)
	os.remove(tts_wav_filename)

def spacestoPluses(text):
	newtext = ''

	for c in text:
		if c == ' ':
			newtext = newtext + '+'
		else:
			newtext = newtext + c

	return newtext


	

# play_wav plays the wave file specified in filename
# if more object oriented this would have self as a parameter
def play_wav(filename): 
	CHUNK = 1024
	wf = wave.open(filename, 'rb')

	# instantiate PyAudio (1)
	# this instantiation is causing the ALSA errors
	# server socket errors
	# jack server error
   	p = pyaudio.PyAudio() 

   	# open stream (2)
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

    # read data
    	data = wf.readframes(CHUNK)

    # play stream (3)
        while data != '':
            stream.write(data)
            data = wf.readframes(CHUNK)

	# stop stream (4)
	# this block threw an error when it was in place.
	# plays wav file fine without it. study documentation?
	    #stream.stop_stream()
	    #tream.close()

	# close PyAudio (5)
        p.terminate()



if __name__ == "__main__":
	main()