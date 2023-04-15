import librosa
import numpy as np

PATH_NAME = "./resources/audio1.wav"

def audio_points():
  x,sr = librosa.load(PATH_NAME,duration=10.0)
  stream = librosa.stream(PATH_NAME,
                          block_length=256,
                          frame_length=2048,
                          hop_length=2048)
  for y_block in stream:
      D_block = librosa.stft(y_block, center=False)
      
  return D_block 

def fft_points():
  return  np.fft.fft(audio_points()) 



  
