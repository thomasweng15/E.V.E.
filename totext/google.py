import tempfile
from pydub import AudioSegment
import requests
import json
import os

from exceptions.exception import NotUnderstoodException

class Google:
	def __init__(self, audio, rate = 44100):
		self.audio = audio
		self.recordingRate = audio.rate() if audio.rate() else rate
		self.text = None

	def get_text(self):
		if not self.text is None:
			return self.text

		# convert wav file to FLAC
		(_,stt_flac_filename) = tempfile.mkstemp('.flac')
		sound = AudioSegment.from_wav(self.audio.filename())
		sound.export(stt_flac_filename, format="flac")

		# send to Google to interpret into text
		google_speech_url = "http://www.google.com/speech-api/v1/recognize?lang=en"
		headers = {'Content-Type': 'audio/x-flac; rate= %d;' % self.recordingRate}
		recording_flac_data = open(stt_flac_filename, 'rb').read()
		r = requests.post(google_speech_url, data=recording_flac_data, headers=headers)

		# housekeeping
		os.remove(stt_flac_filename)
		self.audio.housekeeping()

		# get response as text
		response = r.text

		if not 'hypotheses' in response:
			raise NotUnderstoodException()

		# we are only interested in the most likely utterance
		phrase = json.loads(response)['hypotheses'][0]['utterance']
		print "Heard: " + phrase
		return str(phrase)




