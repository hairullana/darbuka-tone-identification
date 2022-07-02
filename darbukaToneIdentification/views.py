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
import librosa
import numpy as np
from pydub import AudioSegment
import pickle

def index(request):
  return render(request, 'index.html')

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
      toneType = ['dum', 'tak', 'slap']
      datasetTrain = []
      for tone in toneType:
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

      # to display result
      context['basicTone'] = True
      # for tone type
      context['forData'] = [[range(0,20), 'dum'], [range(20,40), 'tak'], [range(40,60), 'slap']]
      # result of identification
      context['resultIdentification'] = resultIdentification
      # display accuracy
      context['accuracy'] = f'Total: {"{:.2f}".format(totalTrueIdentification/60*100)}%<br/>Dum Tone: {"{:.2f}".format(totalDumTrueIdentification/20*100)}%<br/>Tak Tone: {"{:.2f}".format(totalTakTrueIdentification/20*100)}%<br/>Slap Tone: {"{:.2f}".format(totalSlapTrueIdentification/20*100)}%'

    elif 'tonePattern' in request.POST :
      path = 'C:/Coding/darbukaToneIdentification/static/dataset/tonePattern'
      toneType = ['baladi', 'maqsum', 'sayyidi']
      tonePattern = {
        'baladi': ['dum', 'dum', 'tak', 'dum', 'tak'],
        'maqsum': ['dum', 'tak', 'tak', 'dum', 'tak'],
        'sayyidi': ['dum', 'tak', 'dum', 'dum', 'tak']
      }
      resultTonePattern = []
      patternDetect = []
      toneChecks = []

      totalBaladiTrueIdentification = 0
      totalMaqsumTrueIdentification = 0
      totalSayyidiTrueIdentification = 0
      totalTrueIdentification = 0

      # load dataset
      for tone in toneType:
        for data in os.listdir(f'{path}/{tone}'):
          toneData = f'{path}/{tone}/{data}'
          # onset detect
          x, sr = librosa.load(toneData, sr=44100)
          onsetDetection = librosa.onset.onset_detect(x, sr=sr, units='time')
          while len(onsetDetection) > 5 :
            onsetDetection = np.delete(onsetDetection, 0)
          # export onset and detect tone
          toneDetect = []
          toneCheck = []
          i=1
          for onset in onsetDetection:
            newAudio = AudioSegment.from_wav(toneData)
            start = int(onset*1000)
            if i != len(onsetDetection) :
              end = int(onsetDetection[i]*1000)
            else :
              end = int(librosa.get_duration(filename=toneData)*1000)
            newAudio = newAudio[start:end]  
            newAudio.export('temp.wav', format="wav")
            mfcc = mfcc_extract('temp.wav', context['frameLength'], context['overlap'], context['mfccCoefficients'])

            # load model
            frameLength = 'fl=' + request.POST['frameLength']
            overlap = 'o=' + request.POST['overlap'] + '%'
            mfccCoefficients = 'c=' + request.POST['mfccCoefficients']
            modelName = f'{frameLength}_{overlap}_{mfccCoefficients}_model.h5'

            # identification with model
            loaded_model = pickle.load(open(f'C:/Coding/darbukaToneIdentification/static/models/{modelName}', 'rb'))
            resultIdentification = loaded_model.predict(mfcc, context['k'])
            toneDetect.append(resultIdentification)
            toneCheck.append('✅' if tonePattern[tone][i-1] == resultIdentification else '❌')

            
            i += 1

          # check total true identification
          print(toneDetect)
          print(tonePattern[tone])
          if(toneDetect == tonePattern[tone]):
            totalTrueIdentification += 1
            if(tone == 'baladi'):
              totalBaladiTrueIdentification += 1
            if(tone == 'maqsum'):
              totalMaqsumTrueIdentification += 1
            if(tone == 'sayyidi'):
              totalSayyidiTrueIdentification += 1

          print(totalTrueIdentification)

          # check tone pattern is correct or wrong
          if (toneDetect == tonePattern['baladi']):
            patternDetect.append('baladi')
          elif (toneDetect == tonePattern['maqsum']):
            patternDetect.append('maqsum')
          elif (toneDetect == tonePattern['sayyidi']):
            patternDetect.append('sayyidi')
          else:
            patternDetect.append('not detected')


          os.remove('temp.wav')
          resultTonePattern.append(toneDetect)
          toneChecks.append(toneCheck)
      
      # to check result
      context['tonePattern'] = True
      # for tone pattern type result
      context['forData'] = [[range(0,10), 'baladi'], [range(10,20), 'maqsum'], [range(20,30), 'sayyidi']]
      # tone pattern information
      context['tonePatterns'] = tonePattern
      # result tone identification [d, t, t, d, t]
      context['toneDetect'] = resultTonePattern
      # check tone is wrong or not
      context['toneChecks'] = toneChecks
      # check is pattern is wrong or not
      context['patternDetect'] = patternDetect
      # display accuracy
      context['accuracy'] = f'Total: {"{:.2f}".format(totalTrueIdentification/30*100)}%<br/>Baladi Tone: {"{:.2f}".format(totalBaladiTrueIdentification/10*100)}%<br/>Maqsum Tone: {"{:.2f}".format(totalMaqsumTrueIdentification/10*100)}%<br/>Sayyidi Tone: {"{:.2f}".format(totalSayyidiTrueIdentification/10*100)}%'

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