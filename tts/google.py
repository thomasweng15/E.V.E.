from pydub import AudioSegment

import wave
import tempfile
import requests
import os
import sys
import time


class Google:
	"""
	Use the Google Text-to-Speech service to give EVE
	the ability to speak. 
	
	"""
	def say(self, text):
		"""Convert text into speech and then say it"""

		#if convert == 
		if len(text) == 0:
			self.say("Sorry, I don't know.")
			return False

		if len(text) >= 100:
			print "Saying: The result is too long for me to read."
			self.say("The result is too long for me to read.")
			print "Result: " + text
			return False

		# query google text to speech to convert text, store result in temp mp3
		(_,tts_mp3_filename) = tempfile.mkstemp('.mp3')
		r_url = "http://translate.google.com/translate_tts?ie=utf-8&tl=en&q=" \
				+ text.replace(" ", "+")
		try:
			r = requests.get(r_url)
		except requests.exceptions.ConnectionError:
			print "Error: No connection."
			self.play_wav("./wav/internet_err.wav")
			os.remove(tts_mp3_filename)
			return False
		f = open(tts_mp3_filename, 'wb')
		f.write(r.content) 
		f.close()
		# convert mp3 file into wav using pydub
		(_,tts_wav_filename) = tempfile.mkstemp('.wav')
		sound = AudioSegment.from_mp3(tts_mp3_filename)
		sound.export(tts_wav_filename, format="wav")

		print "Saying: " + text
		self.play_wav(tts_wav_filename)

		os.remove(tts_mp3_filename)
		os.remove(tts_wav_filename)
		return True

	def play_wav(self, filename): 
		"""Plays wave file specified in filename."""

		os.system("aplay -q " + filename)
