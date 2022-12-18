import librosa

PATH_NAME = "./resources/audio1.wav"
BLOCK_LENGTH = 256
HOP_LENGTH = 1024


x, sr = librosa.load(PATH_NAME)

stream = librosa.stream(PATH_NAME, block_length=BLOCK_LENGTH, hop_lenght=HOP_LENGTH)

for y_block in stream:
