from multiprocessing import context
import re
from django.shortcuts import render
from DataLatih.functions.automaticClassificationFunc import klasifikasiNada, klasifikasiNadaDasar

def index(request):
  return render(request, 'index.html')

def training(request):
  return render(request, 'training.html')

def identification(request):
  context = {
    'windowLength': 0.02,
    'frameLength': 0.01,
    'k': 1,
  }

  if request.method == 'POST':
    context['windowLength'] = request.POST['windowLength']
    context['frameLength'] = request.POST['frameLength']
    context['k'] = request.POST['k']

    if 'basicTone' in request.POST :
      context['hasilKlasifikasiDum'], context['hasilKlasifikasiTak'], context['hasilKlasifikasiSlap'], context['hasilPresentaseKlasifikasi'] = klasifikasiNada(float(request.POST['windowLength']), float(request.POST['frameLength']), 13, int(request.POST['k']))
    elif 'tonePattern' in request.POST :
      context['hasilKlasifikasiBaladi'], context['hasilKlasifikasiMaqsum'], context['hasilKlasifikasiSayyidi'], context['hasilPresentaseKlasifikasi'] = klasifikasiNadaDasar(float(request.POST['windowLength']), float(request.POST['frameLength']), 13, int(request.POST['k']))

  return render(request, 'identification.html', context)