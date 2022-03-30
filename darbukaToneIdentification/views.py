import os
from django.shortcuts import render
from .functions.automaticClassificationFunc import tonePatternAutomaticIdentification, basicToneAutomaticIdentification
from django.core.files.storage import FileSystemStorage
from .functions.classificationFunc import basicToneIdentification, tonePatternIdentification
from .functions.trainingDataFunc import trainingData
from mfcc_parameters.models import mfcc_parameters
from django.core.cache import cache

def index(request):
  return render(request, 'index.html')

def training(request):
  context = {}
  
  if 'trainingData' in request.POST:
    context['trainingResult'] = trainingData(float(request.POST['frameLength']), float(request.POST['hopLength']), int(request.POST['mfccCoefficient']))
  
  mfcc_parameter = mfcc_parameters.objects.all()[0]
  context['frameLength'] = float(mfcc_parameter.frame_length)
  context['hopLength'] = float(mfcc_parameter.hop_length)
  context['mfccCoefficient'] = int(mfcc_parameter.mfcc_coefficient)

  return render(request, 'training.html', context)

def identification(request):
  cache.clear()
  mfcc_parameter = mfcc_parameters.objects.all()[0]

  context = {
    'frameLength': float(mfcc_parameter.frame_length),
    'hopLength': float(mfcc_parameter.hop_length),
    'mfccCoefficient': int(mfcc_parameter.mfcc_coefficient),
    'k': 3,
  }

  if request.method == 'POST':
    context['k'] = request.POST['k']

    if 'basicToneAutomatic' in request.POST :
      context['dumResult'], context['takResult'], context['slapResult'], context['accuracyResult'] = basicToneAutomaticIdentification(float(context['frameLength']), float(context['hopLength']), int(context['mfccCoefficient']), int(context['k']))
    elif 'tonePatternAutomatic' in request.POST :
      context['baladiResult'], context['maqsumResult'], context['sayyidiResult'], context['accuracyResult'] = tonePatternAutomaticIdentification(float(context['frameLength']), float(context['hopLength']), int(context['mfccCoefficient']), int(context['k']))
    elif 'basicTone' in request.POST and request.FILES:
      dir = 'temp'
      for f in os.listdir(dir):
          os.remove(os.path.join(dir, f))
      inputFile = request.FILES['inputFile']
      fs = FileSystemStorage()
      fs.save('temp.wav', inputFile)

      result = basicToneIdentification('temp/temp.wav', int(context['k']), float(context['frameLength']), float(context['hopLength']), int(context['mfccCoefficient']))

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

      result = tonePatternIdentification('temp/temp.wav', int(context['k']), float(context['frameLength']), float(context['hopLength']), int(context['mfccCoefficient']))

      context['resultTonePattern'] = result
      context['fileLocation'] = '/temp/temp.wav'
      context['filename'] = inputFile.name

  return render(request, 'identification.html', context)