import wave
import pyaudio
import tempfile
import requests
import os
from pydub import AudioSegment

class Google:
	def say(self, text):
		print "Saying: " + text

		# add turn all spaces into pluses
		text = self.spacesToPluses(text)

		# query google text to speech and store result in temp mp3
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

		self.play_wav(tts_wav_filename)

		os.remove(tts_mp3_filename)
		os.remove(tts_wav_filename)

	# convert all spaces in text into pluses to concatenate into url
	def spacesToPluses(self, text):
		return text.replace(" ", "+")


	# play_wav plays the wave file specified in filename
	def play_wav(self, filename): 
		CHUNK = 1024
		wf = wave.open(filename, 'rb')

		# instantiate PyAudio (1)
		# line is causing the error text dump
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
		    #stream.close()

		# close PyAudio (5)
	        p.terminate()
