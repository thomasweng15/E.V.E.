from array import array
from struct import pack

import tempfile
import pyaudio
import sys
import wave
import os


THRESHOLD = 2000
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
SILENCE_DURATION = 55 # end recording after period of silence reaches this value
WAIT_DURATION = 300 # end recording if no input before this value is reached
SPEECH_DURATION = 300 # end recording if too much input

class Microphone:
	"""
	controls all aspects of recording and receiving input 
	from the microphone.
	"""

	def listen(self):
		(_, rec_wav_filename) = tempfile.mkstemp('.wav')
		self.do_wav_recording(rec_wav_filename)
		self.recordedWavFilename = rec_wav_filename
		return self.recordedWavFilename

	def rate(self):
		return RATE

	def filename(self):
		return self.recordedWavFilename

	def housekeeping(self):
		os.remove(self.recordedWavFilename)

	def is_silent(self, sound_data):
		return max(sound_data) < THRESHOLD

	def add_silence(self, sound_data, seconds):
		r = array('h', [0 for i in xrange(int(seconds*RATE))])
		r.extend(sound_data)
		r.extend([0 for i in xrange(int(seconds*RATE))])
		return r

	def record(self):
		p = pyaudio.PyAudio()

		stream = p.open(format = FORMAT,
						channels = CHANNELS, 
						rate = RATE, 
						input = True, 
						frames_per_buffer = CHUNK)

		print("* recording")

		speech_started = False
		speech = 0
		silence_before_speech = 0
		silence_after_speech = 0
		r = array('h')

		while 1:
			sound_data = array('h', stream.read(CHUNK))
			if sys.byteorder == 'big':
				sound_data.byteswap()
			r.extend(sound_data)

			silent = self.is_silent(sound_data)

			if speech_started:
				if silent:
					silence_after_speech += 1
				elif not silent:
					speech += 1

				# break after a period of silence
				if silence_after_speech > SILENCE_DURATION:
					break
				# break after too much input
				if speech > SPEECH_DURATION:
					break
			else: 
				if silent:
					silence_before_speech += 1
				elif not silent: 
					speech_started = True
				# break if no input
				if silence_before_speech > WAIT_DURATION:
					print("Warning: no input. Increase the volume on your mic.")
					break

		print("* done recording")

		sample_width = p.get_sample_size(FORMAT)
		stream.stop_stream() 
		stream.close()
		p.terminate()

		r = self.add_silence(r, 0.5)
		return sample_width, r

	def do_wav_recording(self, rec_wav_filename):
		sample_width, data = self.record()
		data = pack('<' + ('h'*len(data)), *data)

		wf = wave.open(rec_wav_filename, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(sample_width)
		wf.setframerate(RATE)
		wf.writeframes(b''.join(data))
		wf.close()