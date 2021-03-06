import numpy as np, wave, struct, platform, pyaudio, pdb, playsound, os
from scipy.io import wavfile
from scipy.io.wavfile import read as read_wav
from pydub import AudioSegment

if platform.system() == 'Linux':
    from Note_Tone import Note_Tone
elif platform.system() == 'Windows':
    from Utils.Note_Tone import Note_Tone


class Audio_Process():
	def __init__(self, audio_file):
		self.audio_file = audio_file
		############################## Initialize ##################################
		
		# Some Useful Variables
		self.window_size = 2205    # Size of window to be used for detecting silence
		self.beta = 1   # Silence detection parameter
		self.max_notes = 100    # Maximum number of notes in file, for efficiency
		self.sampling_freq = 44100	# Sampling frequency of audio signal
		self.threshold = 600
		self.RATE = 8000

		self.Identified_Notes = []
		self.sound = self.sound_square = np.zeros(0)

		self.__tone = Note_Tone()
		self.array = [self.__tone.notes(i) for i in range(2, 9)]
		self.notes = ['C2', 'Cs2', 'D2', 'Ds2', 'E2', 'F2', 'Fs2', 'G2', 'Gs2', 'A2', 'As2', 'B2',
					  'C3', 'Cs3', 'D3', 'Ds3', 'E3', 'F3', 'Fs3', 'G3', 'Gs3', 'A3', 'As3', 'B3',
					  'C4', 'Cs4', 'D4', 'Ds4', 'E4', 'F4', 'Fs4', 'G4', 'Gs4', 'A4', 'As4', 'B4',
					  'C5', 'Cs5', 'D5', 'Ds5', 'E5', 'F5', 'Fs5', 'G5', 'Gs5', 'A5', 'As5', 'B5',
					  'C6', 'Cs6', 'D6', 'Ds6', 'E6', 'F6', 'Fs6', 'G6', 'Gs6', 'A6', 'As6', 'B6',
					  'C7', 'Cs7', 'D7', 'Ds7', 'E7', 'F7', 'Fs7', 'G7', 'Gs7', 'A7', 'As7', 'B7',
					  'C8', 'Cs8', 'D8', 'Ds8', 'E8', 'F8', 'Fs8', 'G8', 'Gs8', 'A8', 'As8', 'B8']

	def __find_nearest_frequency(self, lst, freq): # This function is throwing error; but re-written works
		#lst = np.asarray(lst)
		idx = (np.abs(lst-freq)).argmin()
		#print(idx)
		return lst[idx]
	
	def __read_audio_file(self, audio_file):
		#pdb.set_trace()
		print ('\nReading Audio File...')
		print('Audio File is: {}'.format(audio_file))

		sound_file = wave.open(audio_file, 'r')
		file_length = sound_file.getnframes()

		self.sound = np.zeros(file_length)
		self.sound_square = np.zeros(file_length)
		for i in range(file_length):
			data = sound_file.readframes(1)
			data = struct.unpack("<h", data)
			self.sound[i] = int(data[0])
			
		self.sound = np.divide(self.sound, float(2**15))	# Normalize data in range -1 to 1
	
	def detect_notes_from_audio(self, audio_file):
		self.__read_audio_file(audio_file)

		######################### DETECTING SILENCE ##################################

		self.sound_square = np.square(self.sound)
		frequency = []
		dft = []
		i = 0
		j = 0
		k = 0    
		# traversing sound_square array with a fixed window_size
		while(i<=len(self.sound_square)-self.window_size):
			s = 0.0
			j = 0
			while(j<=self.window_size):
				s = s + self.sound_square[i+j]
				j = j + 1	
			# detecting the silence waves
			if s < self.threshold:
				if(i-k>self.window_size*4):
					dft = np.array(dft) # applying fourier transform function
					dft = np.fft.fft(self.sound[k:i])
					dft=np.argsort(dft)

					if(dft[0]>dft[-1] and dft[1]>dft[-1]):
						i_max = dft[-1]
					elif(dft[1]>dft[0] and dft[-1]>dft[0]):
						i_max = dft[0]
					else :	
						i_max = dft[1]
					# claculating frequency				
					frequency.append((i_max*self.sampling_freq)/(i-k))
					dft = []
					k = i+1
			i = i + self.window_size

		#print('length',len(frequency))
		#print("frequency")

		for i in frequency :
			#print(i)
			#idx = self.__find_nearest_frequency(self.array, i)
			idx = (np.abs(self.array-i)).argmin()
			#print(idx)
			self.Identified_Notes.append(self.notes[idx])
		return self.Identified_Notes

	def __get_fs_array_from_audio(self, audio_file):
		sampling_rate, data=read_wav(audio_file)
		return (sampling_rate, data)

	def play_audio(self, array=np.zeros(0), audio_file=''):
		if audio_file: # Play Audio direct from file; else from Recording
			_, array = self.__get_fs_array_from_audio(audio_file)
		p = pyaudio.PyAudio()
		stream = p.open(format=pyaudio.paInt16, channels=len(array.shape), rate=self.RATE, output=True)
		stream.write(array.tobytes())
		stream.stop_stream()
		stream.close()
		p.terminate()

	def record(self, duration=3):
		sampling_rate = self.RATE
		nsamples = duration * sampling_rate
		p = pyaudio.PyAudio()
		stream = p.open(format=pyaudio.paInt16, channels=1, rate=sampling_rate, input=True, frames_per_buffer=nsamples)
		buffer = stream.read(nsamples)
		array = np.frombuffer(buffer, dtype='int16')
		stream.stop_stream()
		stream.close()
		p.terminate()
		return array
	
	def record_and_save_to_file(self, duration, output_file=''):
		FORMAT = pyaudio.paInt16
		RATE = 44100
		duration = 5
		CHUNK = duration * RATE

		#print('Record Start')
		audio = pyaudio.PyAudio()
		duration = duration
		stream = audio.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
		Recordframes = []
		for _ in range(0, int(RATE / CHUNK * duration)):
			data = stream.read(CHUNK)
			Recordframes.append(data)
		#print('Record Stop')

		stream.stop_stream()
		stream.close()
		audio.terminate()

		waveFile = wave.open(output_file, 'wb')
		waveFile.setnchannels(1)
		waveFile.setsampwidth(audio.get_sample_size(FORMAT))
		waveFile.setframerate(RATE)
		waveFile.writeframes(b''.join(Recordframes))
		waveFile.close()

	def play_mp3(self, music_dir, mp3_audio_file):
		#pdb.set_trace()
		
		#playsound.playsound(mp3_audio_file, True)

		'''print(mp3_audio_file)
		song = AudioSegment.from_mp3(mp3_audio_file)
		song.export('conv.wav', format='wav')
		self.play_audio(audio_file='conv.wav')'''
		
		os.startfile(os.path.join(music_dir, mp3_audio_file))
