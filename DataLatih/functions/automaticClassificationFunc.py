from . import classificationFunc
from pydub import AudioSegment
import librosa
import os

def basicToneAutomaticIdentification(windowLength, frameLength, mfccCoefficient, k):
  dumResult = []
  takResult = []
  slapResult = []
  totalTrueDum = 0
  totalTrueTak = 0
  totalTrueSlap = 0
  accuracyResult = ""

  # TESTING DUM
  for i in range(20) :
    indeks = i + 51
    filename = 'static/dataset/toneBasic/dum/dum' + str(indeks) + '.wav'
    result = classificationFunc.basicToneIdentification(filename, k, windowLength, frameLength, mfccCoefficient)
    if result == 'DUM':
      totalTrueDum += 1
    dumResult.append(result)

  # TESTING TAK
  for i in range(20) :
    indeks = i + 51
    filename = 'static/dataset/toneBasic/tak/tak' + str(indeks) + '.wav'
    result = classificationFunc.basicToneIdentification(filename, k, windowLength, frameLength, mfccCoefficient)
    if result == 'TAK':
      totalTrueTak += 1
    takResult.append(result)

  # TESTING SLAP
  for i in range(20) :
    indeks = i + 51
    filename = 'static/dataset/toneBasic/slap/slap' + str(indeks) + '.wav'
    result = classificationFunc.basicToneIdentification(filename, k, windowLength, frameLength, mfccCoefficient)
    if result == 'SLAP':
      totalTrueSlap += 1
    slapResult.append(result)
  
  totalTrue = totalTrueDum + totalTrueTak + totalTrueSlap

  accuracyResult += "Total = " + str(totalTrue) + "/60 (" + str("{:.2f}".format(totalTrue/60*100)) + "%)<br/>"
  accuracyResult += "DUM Tone = " + str(totalTrueDum) + "/20 (" + str("{:.2f}".format(totalTrueDum/20*100)) + "%)<br/>"
  accuracyResult += "TAK Tone = " + str(totalTrueTak) + "/20 (" + str("{:.2f}".format(totalTrueTak/20*100)) + "%)<br/>"
  accuracyResult += "SLAP Tone = " + str(totalTrueSlap) + "/20 (" + str("{:.2f}".format(totalTrueSlap/20*100)) + "%)"

  return dumResult, takResult, slapResult, accuracyResult


def tonePatternAutomaticIdentification(windowLength, frameLength, mfccCoefficient, k):
  baladiResult = []
  maqsumResult = []
  sayyidiResult = []
  totalTrueDum = 0
  totalTrueTak = 0
  totalTrueSlap = 0
  accuracyResult = ""

  totalDum = 0
  totalTak = 0
  totalSlap = 0

  tonePatterns = ['baladi', 'maqsum', 'sayyidi']
  baladiTonePattern = ['DUM', 'DUM', 'TAK', 'DUM', 'TAK']
  maqsumTonePattern = ['DUM', 'TAK', 'TAK', 'DUM', 'TAK']
  sayyidiTonePattern = ['DUM', 'TAK', 'DUM', 'DUM', 'TAK']

  for i in range(10):
    for tone in baladiTonePattern:
      if tone == 'DUM':
        totalDum += 1
      elif tone == 'TAK':
        totalTak += 1
      elif tone == 'SLAP':
        totalSlap += 1
    for tone in maqsumTonePattern:
      if tone == 'DUM':
        totalDum += 1
      elif tone == 'TAK':
        totalTak += 1
      elif tone == 'SLAP':
        totalSlap += 1
    for tone in sayyidiTonePattern:
      if tone == 'DUM':
        totalDum += 1
      elif tone == 'TAK':
        totalTak += 1
      elif tone == 'SLAP':
        totalSlap += 1

  for tonePattern in tonePatterns:
    for i in range(10):
      filename = 'static/dataset/tonePattern/' + tonePattern + '2_' + str(i+1) + '.wav'
      x, sr = librosa.load(filename)
      # x, index = librosa.effects.trim(x, top_db=30)
      onsetDetection = librosa.onset.onset_detect(x, sr=sr, units='time')
      j=1
      temp = ''
      resultDetect = []
      toneDetect = []

      for onset in onsetDetection:
        newAudio = AudioSegment.from_wav(filename)
        start = int(onset*1000)
        if j != len(onsetDetection) :
            end = int(onsetDetection[j]*1000)
        else :
            end = int(librosa.get_duration(filename=filename)*1000)
        newAudio = newAudio[start:end]
        newAudio.export('temp.wav', format="wav")
        result = classificationFunc.basicToneIdentification('temp.wav', k, windowLength, frameLength, mfccCoefficient)
        if j != len(onsetDetection):
          temp += result.lower() + '-'
        else :
          temp += result.lower()
        
        if j <= 5 :
          if tonePattern == 'baladi' :
            if result == baladiTonePattern[j-1] :
              toneDetect.append(True)
              if result == 'DUM' :
                totalTrueDum += 1
              elif result == 'TAK' :
                totalTrueTak += 1
              elif result == 'SLAP' :
                totalTrueSlap += 1
            else :
              toneDetect.append(False)
          elif tonePattern == 'maqsum' :
            if result == maqsumTonePattern[j-1] :
              toneDetect.append(True)
              if result == 'DUM' :
                totalTrueDum += 1
              elif result == 'TAK' :
                totalTrueTak += 1
              elif result == 'SLAP' :
                totalTrueSlap += 1
            else :
              toneDetect.append(False)
          elif tonePattern == 'sayyidi' :
            if result == sayyidiTonePattern[j-1] :
              toneDetect.append(True)
              if result == 'DUM' :
                totalTrueDum += 1
              elif result == 'TAK' :
                totalTrueTak += 1
              elif result == 'SLAP' :
                totalTrueSlap += 1
            else :
              toneDetect.append(False)
        else :
          toneDetect.append(False)
      
        j += 1

      resultDetect.append(temp)
      resultDetect.append(toneDetect)

      if tonePattern == 'baladi' :
        baladiResult.append(resultDetect)
      elif tonePattern == 'maqsum' :
        maqsumResult.append(resultDetect)
      elif tonePattern == 'sayyidi' :
        sayyidiResult.append(resultDetect)
      
      
  os.remove('temp.wav')

  accuracyResult += "Total = " + str(totalTrueDum + totalTrueTak + totalTrueSlap) + "/" + str(totalDum + totalTak + totalSlap) + " (" + str("{:.2f}".format((totalTrueDum + totalTrueTak + totalTrueSlap)/150*100)) + "%)<br/>"
  accuracyResult += "DUM Tone = " + str(totalTrueDum) + "/" + str(totalDum) + " (" + str("{:.2f}".format(totalTrueDum/totalDum*100)) + "%)<br/>"
  accuracyResult += "TAK Tone = " + str(totalTrueTak) + "/" + str(totalTak) + " (" + str("{:.2f}".format(totalTrueTak/totalTak*100)) + "%)<br/>"
  if totalSlap != 0:
    accuracyResult += "SLAP Tone = " + str(totalTrueSlap) + "/" + str(totalSlap) + " (" + str("{:.2f}".format(totalTrueSlap/totalSlap*100)) + "%)"

  return baladiResult, maqsumResult, sayyidiResult, accuracyResult