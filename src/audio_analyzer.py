import librosa
import numpy as np

PATH_NAME = "./resources/audio1.wav"

def audio_points():
  x,sr = librosa.load(PATH_NAME,duration=10.0)
  return x 

def fft_points():
  return np.fft.fft(audio_points()) 


  
  
