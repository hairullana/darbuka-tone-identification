from multiprocessing import context
import re
from django.shortcuts import render
from DataLatih.functions.automaticClassificationFunc import klasifikasiNada, klasifikasiNadaDasar

def index(request):
  data = {
    'windowLength': 0.02,
    'frameLength': 0.01,
    'mfccCoefficients': 13,
    'k': 1
  }

  if request.method == 'POST':
    if 'automaticClassification' in request.POST :
      data['hasilKlasifikasiDum'], data['hasilKlasifikasiTak'], data['hasilKlasifikasiSlap'], data['hasilPresentaseKlasifikasi'] = klasifikasiNada(data['windowLength'], data['frameLength'], data['mfccCoefficients'], data['k'])
      data['text'] = klasifikasiNadaDasar(data['windowLength'], data['frameLength'], data['mfccCoefficients'], data['k'])
    else :
      data['windowLength'] = request.POST['windowLength']
      data['frameLength'] = request.POST['frameLength']
      data['mfccCoefficients'] = request.POST['mfccCoefficients']
      data['k'] = request.POST['k']

  return render(request, 'index.html', data)

def training(request):
  return render(request, 'training.html')

def basicTone(request):
  context = {
    'title': 'Basic Tone Identification',
    'description': 'Identify the basic hadrah tone (DUM, TAK/KA, SLAP) with Mel Frequency Cepstral Coefficient (MFCC) and K-Nearest Neighbor (KNN) algorithm',
  }

  return render(request, 'identification.html', context)

def tonePattern(request):
  context = {
    'title': 'Tone Pattern Identification',
    'description': 'Identify hadrah tone pattern (DUM, TAK/KA, SLAP) with Mel Frequency Cepstral Coefficient (MFCC), Onset Detection and K-Nearest Neighbor (KNN) algorithm'
  }

  return render(request, 'identification.html', context)