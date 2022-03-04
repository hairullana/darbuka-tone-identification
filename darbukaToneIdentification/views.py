import os
from django.shortcuts import render
from darbukaToneIdentification.functions.automaticClassificationFunc import basicToneAutomaticIdentification, tonePatternAutomaticIdentification
from django.core.files.storage import FileSystemStorage
from darbukaToneIdentification.functions.classificationFunc import basicToneIdentification, tonePatternIdentification
from darbukaToneIdentification.functions.trainingDataFunc import trainingData
from mfcc_parameters.models import mfcc_parameters


def index(request):
  return render(request, 'index.html')

def training(request):
  mfcc_parameter = mfcc_parameters.objects.all()[0]

  context = {
    'windowLength': mfcc_parameter.window_length,
    'frameLength': mfcc_parameter.frame_length,
    'mfccCoefficient': mfcc_parameter.mfcc_coefficient,
  }

  if 'trainingData' in request.POST:
    context['trainingResult'] = trainingData(float(request.POST['windowLength']), float(request.POST['frameLength']), int(request.POST['mfccCoefficient']))

  return render(request, 'training.html', context)

def identification(request):
  mfcc_parameter = mfcc_parameters.objects.all()[0]

  context = {
    'windowLength': mfcc_parameter.window_length,
    'frameLength': mfcc_parameter.frame_length,
    'mfccCoefficient': mfcc_parameter.mfcc_coefficient,
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
      dir = 'temp'
      for f in os.listdir(dir):
          os.remove(os.path.join(dir, f))
      inputFile = request.FILES['inputFile']
      fs = FileSystemStorage()
      fs.save('temp.wav', inputFile)

      result = basicToneIdentification('temp/temp.wav', int(request.POST['k']), float(request.POST['windowLength']), float(request.POST['frameLength']), 13)

      context['resultBasicTone'] = result
      context['fileLocation'] = '/temp/temp.wav'
      context['filename'] = inputFile.name
    elif 'tonePattern' in request.POST and request.FILES:
      dir = 'temp'
      for f in os.listdir(dir):
          os.remove(os.path.join(dir, f))
      inputFile = request.FILES['inputFile']
      fs = FileSystemStorage()
      fs.save('temp.wav', inputFile)

      result = tonePatternIdentification('temp/temp.wav', int(request.POST['k']), float(request.POST['windowLength']), float(request.POST['frameLength']), 13)

      context['resultTonePattern'] = result
      context['fileLocation'] = '/temp/temp.wav'
      context['filename'] = inputFile.name

  return render(request, 'identification.html', context)