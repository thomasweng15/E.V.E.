#!/usr/bin/python
# -*- coding: utf-8 -*-

from array import array
from struct import pack

import tempfile
import pyaudio
import sys
import wave
import os

THRESHOLD = 1000
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

class Microphone:
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
		"Returns True if below 'silent' threshold"
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

		num_silent = 0
		sound_started = False

		r = array('h')

		print("* recording")

		while 1:
			sound_data = array('h', stream.read(CHUNK))
			if sys.byteorder == 'big':
				sound_data.byteswap()
			r.extend(sound_data)

			silent = self.is_silent(sound_data)

			if silent and sound_started:
				num_silent += 1
			#elif not silent and sound_started:
			#	num_silent = 0
			elif not silent and not sound_started:
				sound_started = True

			if sound_started and num_silent > 30:
				break


		"""frames = []
		for i in range(0, int(RATE / CHUNK * duration)):
			data = stream.read(CHUNK)
			frames.append(data)
"""
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