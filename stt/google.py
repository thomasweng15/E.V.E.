from ex.exception import NotUnderstoodException
from ex.exception import ConnectionLostException
from pydub import AudioSegment

import tempfile
import requests
import json
import os
import sys


class Google:
	"""
	uses the Google Speech-to-Text service
	to translate voice input into text,
	so that it can be parsed by the program.
	"""

	def __init__(self, audio, rate = 44100):
		self.audio = audio
		self.rec_rate = audio.rate() if audio.rate() else rate
		self.text = None

	def get_text(self):
		if not self.text is None:
			return self.text

		# convert wav file to FLAC
		(_,stt_flac_filename) = tempfile.mkstemp('.flac')
		sound = AudioSegment.from_wav(self.audio.filename())
		sound.export(stt_flac_filename, format="flac")

		# send to Google to interpret into text
		g_url = "http://www.google.com/speech-api/v1/recognize?lang=en"
		headers = {'Content-Type': 'audio/x-flac; rate= %d;' % self.rec_rate}
		recording_flac_data = open(stt_flac_filename, 'rb').read()
		try:
			r = requests.post(g_url, data=recording_flac_data, headers=headers)
		except requests.exceptions.ConnectionError:
			raise ConnectionLostException()

		os.remove(stt_flac_filename)
		self.audio.housekeeping()

		response = r.text

		if not 'hypotheses' in response:
			raise NotUnderstoodException()

		# we are only interested in the most likely utterance
		phrase = json.loads(response)['hypotheses'][0]['utterance']
		print "Heard: " + phrase
		return str(phrase)




