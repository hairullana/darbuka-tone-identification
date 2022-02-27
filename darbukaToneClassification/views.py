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