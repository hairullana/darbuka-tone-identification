import librosa
import librosa.feature

# MFCC
def mfcc_extract(filename, windowLength, frameLength, mfccCoefficients):
  windowLength, frameLength, mfccCoefficients
  # LOAD SONG WITH 44,1K
  y, sr  = librosa.load(filename, sr=44100)
  # SILENCE REMOVAL
  yt, index = librosa.effects.trim(y, top_db=30)
  # WINDOW WIDTH (OVERLAPPING) = 20ms
  a=int(windowLength*sr)
  # FRAME LENGTH = 10ms
  b=int(frameLength*sr)
  # EXTRACTION
  mfcc = librosa.feature.mfcc(y=yt, sr=sr, n_mfcc=mfccCoefficients,n_fft=a,hop_length=b)
  return mfcc