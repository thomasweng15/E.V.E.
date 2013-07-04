from pydub import AudioSegment

import wave
import tempfile
import requests
import os


class Google:
	"""
	Use the Google Text-to-Speech service to give EVE
	the ability to speak. 
	
	"""
	def say(self, text):
		"""Speak text string by converting to wav and then playing it"""
		wav_file = self.convert_text_to_wav(text)
		if wav_file == False:
			return False
		print "Saying: " + text
		self.play_wav(wav_file)
		os.remove(wav_file)
		return True

	def convert_text_to_wav(self, text):
		"""Convert text string into wav file."""
		if len(text) == 0:
			self.say("Sorry, I don't know.")
			return False

		if len(text) >= 100:
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
		os.remove(tts_mp3_filename)
		return tts_wav_filename

	def play_wav(self, filename): 
		"""Plays wav file specified in filename."""
		os.system("aplay -q " + filename)
