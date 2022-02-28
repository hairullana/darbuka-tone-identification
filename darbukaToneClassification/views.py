from multiprocessing import context
import re
from django.shortcuts import render
from DataLatih.functions.automaticClassificationFunc import klasifikasiNada, klasifikasiNadaDasar

def index(request):
  return render(request, 'index.html')

def training(request):
  return render(request, 'training.html')

def basicTone(request):
  context = {
    'title': 'Basic Tone Identification',
    'description': 'Identify the basic hadrah tone (DUM, TAK/KA, SLAP) with Mel Frequency Cepstral Coefficient (MFCC) and K-Nearest Neighbor (KNN) algorithm',
    'windowLength': 0.02,
    'frameLength': 0.01,
    'k': 1,
    'automaticIdentification': 'basicTone',
  }

  if request.method == 'POST':
    if 'basicTone' in request.POST :
      context['hasilKlasifikasiDum'], context['hasilKlasifikasiTak'], context['hasilKlasifikasiSlap'], context['hasilPresentaseKlasifikasi'] = klasifikasiNada(context['windowLength'], context['frameLength'], 13, context['k'])
    else :
      context['windowLength'] = request.POST['windowLength']
      context['frameLength'] = request.POST['frameLength']
      context['k'] = request.POST['k']

  return render(request, 'identification.html', context)

def tonePattern(request):
  context = {
    'title': 'Tone Pattern Identification',
    'description': 'Identify hadrah tone pattern (DUM, TAK/KA, SLAP) with Mel Frequency Cepstral Coefficient (MFCC), Onset Detection and K-Nearest Neighbor (KNN) algorithm',
    'windowLength': 0.02,
    'frameLength': 0.01,
    'k': 1,
    'automaticIdentification': 'tonePattern',
  }

  if request.method == 'POST':
    if 'tonePattern' in request.POST :
      context['text'] = klasifikasiNadaDasar(context['windowLength'], context['frameLength'], 13, context['k'])
    else :
      context['windowLength'] = request.POST['windowLength']
      context['frameLength'] = request.POST['frameLength']
      context['k'] = request.POST['k']

  return render(request, 'identification.html', context)