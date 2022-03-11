import librosa
import librosa.feature

# MFCC
def mfcc_extract(filename, frameLength, hopLength, mfccCoefficient):
  frameLength, hopLength, mfccCoefficient
  # LOAD SONG WITH 44,1K
  y, sr  = librosa.load(filename, sr=44100)
  # SILENCE REMOVAL
  yt, index = librosa.effects.trim(y, top_db=10)
  # WINDOW WIDTH (OVERLAPPING) = 20ms
  frame_length=int(frameLength*sr)
  # FRAME LENGTH = 10ms
  hop_length=int(hopLength*sr)
  # EXTRACTION
  mfcc = librosa.feature.mfcc(y=yt, sr=sr, n_mfcc=mfccCoefficient,n_fft=frame_length,hop_length=hop_length)
  return mfcc