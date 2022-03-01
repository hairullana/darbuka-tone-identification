import os
from django.shortcuts import render
from DataLatih.functions.automaticClassificationFunc import basicToneAutomaticIdentification, tonePatternAutomaticIdentification
from django.core.files.storage import FileSystemStorage
from DataLatih.functions.classificationFunc import basicToneIdentification, tonePatternIdentification


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
      context['dumResult'], context['takResult'], context['slapResult'], context['accuracyResult'] = basicToneAutomaticIdentification(float(request.POST['windowLength']), float(request.POST['frameLength']), 13, int(request.POST['k']))
    elif 'tonePatternAutomatic' in request.POST :
      context['baladiResult'], context['maqsumResult'], context['sayyidiResult'], context['accuracyResult'] = tonePatternAutomaticIdentification(float(request.POST['windowLength']), float(request.POST['frameLength']), 13, int(request.POST['k']))
    elif 'basicTone' in request.POST and request.FILES:
      dir = 'media'
      for f in os.listdir(dir):
          os.remove(os.path.join(dir, f))
      inputFile = request.FILES['inputFile']
      fs = FileSystemStorage()
      fs.save('temp.wav', inputFile)

      result = basicToneIdentification('media/temp.wav', int(request.POST['k']), float(request.POST['windowLength']), float(request.POST['frameLength']), 13)

      context['resultBasicTone'] = result
      context['fileLocation'] = '/media/temp.wav'
      context['filename'] = inputFile.name
    elif 'tonePattern' in request.POST and request.FILES:
      dir = 'media'
      for f in os.listdir(dir):
          os.remove(os.path.join(dir, f))
      inputFile = request.FILES['inputFile']
      fs = FileSystemStorage()
      fs.save('temp.wav', inputFile)

      result = tonePatternIdentification('media/temp.wav', int(request.POST['k']), float(request.POST['windowLength']), float(request.POST['frameLength']), 13)

      context['resultTonePattern'] = result
      context['fileLocation'] = '/media/temp.wav'
      context['filename'] = inputFile.name

  return render(request, 'identification.html', context)