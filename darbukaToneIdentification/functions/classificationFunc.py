import os
import math
import numpy as np
from .graph import get_graph
from .mfccFunc import mfcc_extract, flatten_extraction
from dataset.models import dataset
import librosa
import librosa.display
from pydub import AudioSegment
import matplotlib.pylab as plt

# COLLECTING TRAINING DATASET IN DB
data = dataset.objects.all()

dum = []
tak = []
slap = []

for x in data:
  dataExtraction = x.extraction
  if x.tone == 'dum' :
    dum.append(np.fromstring(dataExtraction.strip('[]'), dtype=float, sep=' '))
  elif x.tone == 'tak' :
    tak.append(np.fromstring(dataExtraction.strip('[]'), dtype=float, sep=' '))
  elif x.tone == 'slap' :
    slap.append(np.fromstring(dataExtraction.strip('[]'), dtype=float, sep=' '))

# CLASSIFICATION
def basicToneIdentification(filename, k, frameLength, overlap, mfccTotalFeature, isSingleIdentification) :
  audio,_ = librosa.load(filename, sr=44100)

  audioPlot = False
  mfccPlot = False
  knnPlot = False
  
  # MFCC
  testing_no_flatten = mfcc_extract(filename, frameLength, overlap, mfccTotalFeature, flatten=False)
  testing = mfcc_extract(filename, frameLength, overlap, mfccTotalFeature, flatten=True)
  # CALCULATE DISTANCE
  data_jarak = []
  for nada_dum in dum :
    total = 0
    for i in range(mfccTotalFeature) :
      total += pow((nada_dum[i] - testing[i]),2)
    euclidean_distance = math.sqrt(total)
    data_jarak.append(euclidean_distance)
  for nada_tak in tak :
    total = 0
    for i in range(mfccTotalFeature) :
      total += pow((nada_tak[i] - testing[i]),2)
    euclidean_distance = math.sqrt(total)
    data_jarak.append(euclidean_distance)
  for nada_slap  in slap :
    total = 0
    for i in range(mfccTotalFeature) :
      total += pow((nada_slap[i] - testing[i]),2)
    euclidean_distance = math.sqrt(total)
    data_jarak.append(euclidean_distance)
  
  # KNN
  data_jarak2 = data_jarak
  indeks = []
  for knn in range(k) :
    smallest = 0
    indeks.append(0)
    for i in range(len(data_jarak2)) :
      if i not in indeks and data_jarak2[i] <= data_jarak2[smallest] :
        smallest = i
        indeks[knn] = smallest

  # CHOOSE MOST K
  k_dum = 0
  k_tak = 0
  k_slap = 0
  
  for i in range(len(indeks)) :
    if indeks[i] < 50 :
      k_dum += 1
    elif indeks[i] < 100 :
      k_tak += 1
    elif indeks[i] < 150 :
      k_slap += 1

  if k_dum > k_tak and k_dum > k_slap :
    result = 'DUM'
  elif k_tak > k_dum and k_tak > k_slap :
    result = 'TAK'
  elif k_slap > k_dum and k_slap > k_tak :
    result = 'SLAP'
  elif k_dum == k_tak :
    result = 'DUM / TAK'
  elif k_dum == k_slap :
    result = 'DUM / SLAP'
  elif k_tak == k_slap :
    result = 'TAK / SLAP'
  else :
    result = 'DUM / TAK / SLAP'
  
  if isSingleIdentification:
    plt.figure(figsize=(15,5))
    plt.title('Audio Plot')
    plt.plot(np.linspace(0, len(audio) / 44100, num=len(audio)), audio)
    audioPlot = get_graph()

    plt.figure(figsize=(15,5))
    plt.title('MFCC Extraction')
    librosa.display.specshow(testing_no_flatten, x_axis='time', sr=44100)
    plt.colorbar(format="%+2f")
    mfccPlot = get_graph()

    plt.figure(figsize=(15,5))
    plt.title('KNN Classification')
    plt.bar(['DUM', 'TAK', 'SLAP'], [k_dum, k_tak, k_slap])
    knnPlot = get_graph()
  
  return result, audioPlot, mfccPlot, knnPlot

def tonePatternIdentification(filename, k, frameLength, overlap, mfccCoefficient, isSingleIdentification):
  x, sr = librosa.load(filename, sr=44100)
  onsetDetection = librosa.onset.onset_detect(x, sr=sr, units='time')
  while len(onsetDetection) > 5 :
    onsetDetection = np.delete(onsetDetection, 0)
  
  audioPlotBeforeOnsetDetection = False

  if isSingleIdentification:
    plt.figure(figsize=(15,5))
    plt.title('Audio Plot (Before Onset Detection)')
    plt.plot(np.linspace(0, len(x) / 44100, num=len(x)), x)
    audioPlotBeforeOnsetDetection = get_graph()

  toneDetect = []
  plots = []
  j=1

  for onset in onsetDetection:
    plot = []
    newAudio = AudioSegment.from_wav(filename)
    start = int(onset*1000)
    if j != len(onsetDetection) :
      end = int(onsetDetection[j]*1000)
    else :
      end = int(librosa.get_duration(filename=filename)*1000)
    newAudio = newAudio[start:end]  
    newAudio.export('temp.wav', format="wav")
    if isSingleIdentification :
      result, audioPlot, mfccPlot, knnPlot = basicToneIdentification('temp.wav', k, frameLength, overlap, mfccCoefficient, True)
    else :
      result, audioPlot, mfccPlot, knnPlot = basicToneIdentification('temp.wav', k, frameLength, overlap, mfccCoefficient, False)

    toneDetect.append(result)
    plot.append(audioPlot)
    plot.append(mfccPlot)
    plot.append(knnPlot)
    plots.append(plot)
    
    j += 1

  os.remove('temp.wav')
  return audioPlotBeforeOnsetDetection, toneDetect, plots