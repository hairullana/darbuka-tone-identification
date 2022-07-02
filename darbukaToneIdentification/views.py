from email.mime import audio
import os
from django.shortcuts import render
from .functions.automaticClassificationFunc import tonePatternAutomaticIdentification, basicToneAutomaticIdentification
from django.core.files.storage import FileSystemStorage
from .functions.classificationFunc import basicToneIdentification, tonePatternIdentification
from .functions.trainingDataFunc import trainingData
from .functions.mfccFunc import mfcc_extract
from mfcc_parameters.models import mfcc_parameters
from django.core.cache import cache
import math
import pickle

def index(request):
  return render(request, 'index.html')

def training(request):
  context = {}
  
  if 'trainingData' in request.POST:
    context['trainingResult'] = trainingData(float(request.POST['frameLength']), float(request.POST['overlap']), int(request.POST['mfccCoefficient']))
  
  mfcc_parameter = mfcc_parameters.objects.all()[0]
  context['frameLength'] = float(mfcc_parameter.frame_length)
  context['overlap'] = float(mfcc_parameter.overlap)
  context['mfccCoefficient'] = int(mfcc_parameter.mfcc_coefficient)

  return render(request, 'training.html', context)

def developerIdentification(request):
  cache.clear()
  context = {
    'frameLength': 0.01,
    'overlap': 50,
    'mfccCoefficients': 16,
    'k': 3
  }

  if request.method == 'POST':
    context['frameLength'] = float(request.POST['frameLength'])
    context['overlap'] = float(request.POST['frameLength']) / 100 * float(request.POST['overlap'])
    context['mfccCoefficients'] = int(request.POST['mfccCoefficients'])
    context['k'] = int(request.POST['k'])

    if 'basicTone' in request.POST :
      # load dataset
      path = 'C:/Coding/darbukaToneIdentification/static/dataset/toneBasic/test'
      tone_type = ['dum', 'tak', 'slap']
      datasetTrain = []
      for tone in tone_type:
        for data in os.listdir(f'{path}/{tone}'):
          toneData = f'{path}/{tone}/{data}'
          extract = mfcc_extract(toneData, context['frameLength'], context['overlap'], context['mfccCoefficients'])
          datasetTrain.append([extract, tone])
      
      # split test data
      extractionTest = []
      labelTest = []
      for features, label in datasetTrain:
        extractionTest.append(features)
        labelTest.append(label)

      # load model
      frameLength = 'fl=' + request.POST['frameLength']
      overlap = 'o=' + request.POST['overlap'] + '%'
      mfccCoefficients = 'c=' + request.POST['mfccCoefficients']
      modelName = f'{frameLength}_{overlap}_{mfccCoefficients}_model.h5'

      # identification with model
      loaded_model = pickle.load(open(f'C:/Coding/darbukaToneIdentification/static/models/{modelName}', 'rb'))
      resultIdentification = loaded_model.predicts(extractionTest, context['k'])

      # return variable to templates
      totalTrueIdentification = 0
      totalDumTrueIdentification = 0
      totalTakTrueIdentification = 0
      totalSlapTrueIdentification = 0

      for i in range(len(resultIdentification)):
        if resultIdentification[i] == labelTest[i]:
          totalTrueIdentification += 1
          if labelTest[i] == 'dum':
            totalDumTrueIdentification += 1
          if labelTest[i] == 'tak':
            totalTakTrueIdentification += 1
          if labelTest[i] == 'slap':
            totalSlapTrueIdentification += 1

      context['basicTone'] = True
      context['forData'] = [[range(0,20), 'dum'], [range(20,40), 'tak'], [range(40,60), 'slap']]
      context['resultIdentification'] = resultIdentification
      context['accuracy'] = f'Total: {"{:.2f}".format(totalTrueIdentification/60*100)}%<br/>Dum Tone: {"{:.2f}".format(totalDumTrueIdentification/20*100)}%<br/>Tak Tone: {"{:.2f}".format(totalTakTrueIdentification/20*100)}%<br/>Slap Tone: {"{:.2f}".format(totalSlapTrueIdentification/20*100)}%'


    elif 'tonePattern' in request.POST :
      context['audioPlotBeforeOnsetDetection'], context['baladiResult'], context['maqsumResult'], context['sayyidiResult'], context['accuracyResult'], context['plots'] = tonePatternAutomaticIdentification(float(context['frameLength']), float(context['overlap']), int(context['mfccCoefficient']), int(context['k']))

  return render(request, 'identification-developer.html', context)

def userIdentification(request):
  cache.clear()
  mfcc_parameter = mfcc_parameters.objects.all()[0]

  context = {
    'frameLength': float(mfcc_parameter.frame_length),
    'overlap': float(mfcc_parameter.overlap),
    'mfccCoefficient': int(mfcc_parameter.mfcc_coefficient),
    'k': 3,
  }

  if request.method == 'POST':
    context['k'] = request.POST['k']

    if 'basicToneAutomatic' in request.POST :
      context['dumResult'], context['takResult'], context['slapResult'], context['accuracyResult'] = basicToneAutomaticIdentification(float(context['frameLength']), float(context['overlap']), int(context['mfccCoefficient']), int(context['k']))
    elif 'tonePatternAutomatic' in request.POST :
      context['audioPlotBeforeOnsetDetection'], context['baladiResult'], context['maqsumResult'], context['sayyidiResult'], context['accuracyResult'], context['plots'] = tonePatternAutomaticIdentification(float(context['frameLength']), float(context['overlap']), int(context['mfccCoefficient']), int(context['k']))
    elif 'basicTone' in request.POST and request.FILES:
      dir = 'temp'
      for f in os.listdir(dir):
          os.remove(os.path.join(dir, f))
      inputFile = request.FILES['inputFile']
      fs = FileSystemStorage()
      fs.save('temp.wav', inputFile)

      result, audioPlot, mfccPlot, knnPlot = basicToneIdentification('temp/temp.wav', int(context['k']), float(context['frameLength']), float(context['overlap']), int(context['mfccCoefficient']), True)

      if request.POST['basicToneType'] == result :
        context['toneResult'] = '✅'
      else :
        context['toneResult'] = '❌'

      context['basicToneType'] = request.POST['basicToneType']
      context['audioPlot'] = audioPlot
      context['mfccPlot'] = mfccPlot
      context['knnPlot'] = knnPlot
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

      audioPlotBeforeOnsetDetection, result, plots = tonePatternIdentification('temp/temp.wav', int(context['k']), float(context['frameLength']), float(context['overlap']), int(context['mfccCoefficient']), True)

      if request.POST['tonePatternType'] == 'BALADI' :
        tonePattern = ['DUM', 'DUM', 'TAK', 'DUM', 'TAK']
      elif request.POST['tonePatternType'] == 'MAQSUM' :
        tonePattern = ['DUM', 'TAK', 'TAK', 'DUM', 'TAK']
      elif request.POST['tonePatternType'] == 'SAYYIDI' :
        tonePattern = ['DUM', 'TAK', 'DUM', 'DUM', 'TAK']
      
      tonePatternResult = []
      for i in range(5):
        if tonePattern[i] == result[i]:
          tonePatternResult.append('✅')
        else :
          tonePatternResult.append('❌')

      context['tonePatternType'] = request.POST['tonePatternType']
      context['tonePattern'] = tonePattern
      context['tonePatternResult'] = tonePatternResult
      context['audioPlotBeforeOnsetDetection'] = audioPlotBeforeOnsetDetection
      context['plots'] = plots
      context['resultTonePattern'] = result
      context['fileLocation'] = '/temp/temp.wav'
      context['filename'] = inputFile.name

  return render(request, 'identification.html', context)