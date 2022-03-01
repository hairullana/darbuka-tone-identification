import os
from django.shortcuts import render
from DataLatih.functions.automaticClassificationFunc import klasifikasiNada, klasifikasiNadaDasar
from django.core.files.storage import FileSystemStorage
from DataLatih.functions.classificationFunc import klasifikasi, tonePatternIdentification


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

    if 'basicToneAutomatic' in request.POST :
      context['hasilKlasifikasiDum'], context['hasilKlasifikasiTak'], context['hasilKlasifikasiSlap'], context['hasilPresentaseKlasifikasi'] = klasifikasiNada(float(request.POST['windowLength']), float(request.POST['frameLength']), 13, int(request.POST['k']))
    elif 'tonePatternAutomatic' in request.POST :
      context['hasilKlasifikasiBaladi'], context['hasilKlasifikasiMaqsum'], context['hasilKlasifikasiSayyidi'], context['hasilPresentaseKlasifikasi'] = klasifikasiNadaDasar(float(request.POST['windowLength']), float(request.POST['frameLength']), 13, int(request.POST['k']))
    elif 'basicTone' in request.POST and request.FILES:
      dir = 'media'
      for f in os.listdir(dir):
          os.remove(os.path.join(dir, f))
      inputFile = request.FILES['inputFile']
      fs = FileSystemStorage()
      fs.save('temp.wav', inputFile)

      hasil, k_dum, k_tak, k_slap, indeks = klasifikasi('media/temp.wav', int(request.POST['k']), float(request.POST['windowLength']), float(request.POST['frameLength']), 13)

      context['resultBasicTone'] = hasil
      context['fileLocation'] = '/media/temp.wav'
      context['filename'] = inputFile.name
    elif 'tonePattern' in request.POST and request.FILES:
      dir = 'media'
      for f in os.listdir(dir):
          os.remove(os.path.join(dir, f))
      inputFile = request.FILES['inputFile']
      fs = FileSystemStorage()
      fs.save('temp.wav', inputFile)

      hasil = tonePatternIdentification('media/temp.wav', int(request.POST['k']), float(request.POST['windowLength']), float(request.POST['frameLength']), 13)

      context['resultTonePattern'] = hasil
      context['fileLocation'] = '/media/temp.wav'
      context['filename'] = inputFile.name

  return render(request, 'identification.html', context)