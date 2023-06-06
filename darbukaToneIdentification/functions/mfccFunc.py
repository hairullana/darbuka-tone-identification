import librosa
import librosa.feature
import numpy as np

# MFCC
def mfcc_extract(filename, frameLength, overlap, mfccCoefficient, flatten=True):
  overlap = frameLength / 100 * overlap
  hopLength = frameLength - overlap
  y, sr  = librosa.load(filename, sr=44100)
  # SILENCE REMOVAL
  yt, index = librosa.effects.trim(y, top_db=10)
  frame_length=int(frameLength*sr)
  hop_length=int(hopLength*sr)
  mfcc = librosa.feature.mfcc(y=yt, sr=sr, n_mfcc=mfccCoefficient,n_fft=frame_length,hop_length=hop_length)
  
  if flatten == False:
    return mfcc
  else:
    return flatten_extraction(mfcc)

def flatten_extraction(mfcc):
  return np.mean(mfcc, axis=1)