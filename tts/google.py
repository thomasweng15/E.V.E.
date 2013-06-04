#!/usr/bin/python
# -*- coding: utf-8 -*-

from pydub import AudioSegment

import wave
import pyaudio
import tempfile
import requests
import os
import sys


class Google:
	def say(self, text):
		if len(text) >= 100:
			print "Saying: The result is too long for me to read."
			self.say("The result is too long for me to read.")
			print "Result: " + text
			return 

		print "Saying: " + text

		# query google text to speech and store result in temp mp3
		(_,tts_mp3_filename) = tempfile.mkstemp('.mp3')
		r_url = "http://translate.google.com/translate_tts?ie=utf-8&tl=en&q=" \
				+ text.replace(" ", "+")
		r = requests.get(r_url)
		f = open(tts_mp3_filename, 'wb')
		f.write(r.content) 
		f.close()

		# convert mp3 file into wav using pydub
		(_,tts_wav_filename) = tempfile.mkstemp('.wav')
		sound = AudioSegment.from_mp3(tts_mp3_filename)
		sound.export(tts_wav_filename, format="wav")

		self.play_wav(tts_wav_filename)

		os.remove(tts_mp3_filename)
		os.remove(tts_wav_filename)

	# play_wav plays the wave file specified in filename
	def play_wav(self, filename): 
		CHUNK = 1024
		wf = wave.open(filename, 'rb')

		p = pyaudio.PyAudio() # line is causing the error text dump

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
		stream.stop_stream()
		stream.close()

		p.terminate()