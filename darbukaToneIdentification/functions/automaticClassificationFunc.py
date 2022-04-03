from .classificationFunc import basicToneIdentification, tonePatternIdentification
from django.core.cache import cache

def basicToneAutomaticIdentification(frameLength, hopLength, mfccCoefficient, k):
  cache.clear()
  dumResult = []
  takResult = []
  slapResult = []
  totalTrueDum = 0
  totalTrueTak = 0
  totalTrueSlap = 0
  accuracyResult = ""

  totalTesting = 20

  # TESTING DUM
  for i in range(totalTesting) :
    indeks = i + 51
    filename = 'D:/Ngoding/darbukaToneIdentification/static/dataset/toneBasicNoise/dum/dum' + str(indeks) + '.wav'
    result, audioPlot, mfccPlot, knnPlot = basicToneIdentification(filename, k, frameLength, hopLength, mfccCoefficient, False)
    if result == 'DUM':
      totalTrueDum += 1
    dumResult.append(result)

  # TESTING TAK
  for i in range(totalTesting) :
    indeks = i + 51
    filename = 'D:/Ngoding/darbukaToneIdentification/static/dataset/toneBasicNoise/tak/tak' + str(indeks) + '.wav'
    result, audioPlot, mfccPlot, knnPlot = basicToneIdentification(filename, k, frameLength, hopLength, mfccCoefficient, False)
    if result == 'TAK':
      totalTrueTak += 1
    takResult.append(result)

  # TESTING SLAP
  for i in range(totalTesting) :
    indeks = i + 51
    filename = 'D:/Ngoding/darbukaToneIdentification/static/dataset/toneBasicNoise/slap/slap' + str(indeks) + '.wav'
    result, audioPlot, mfccPlot, knnPlot = basicToneIdentification(filename, k, frameLength, hopLength, mfccCoefficient, False)
    if result == 'SLAP':
      totalTrueSlap += 1
    slapResult.append(result)
  
  totalTrue = totalTrueDum + totalTrueTak + totalTrueSlap

  accuracyResult += "Total = " + str(totalTrue) + "/" + str(totalTesting*3) + " (" + str("{:.2f}".format(totalTrue/(totalTesting*3)*100)) + "%)<br/>"
  accuracyResult += "DUM Tone = " + str(totalTrueDum) + "/" + str(totalTesting) + " (" + str("{:.2f}".format(totalTrueDum/totalTesting*100)) + "%)<br/>"
  accuracyResult += "TAK Tone = " + str(totalTrueTak) + "/" + str(totalTesting) + " (" + str("{:.2f}".format(totalTrueTak/totalTesting*100)) + "%)<br/>"
  accuracyResult += "SLAP Tone = " + str(totalTrueSlap) + "/" + str(totalTesting) + " (" + str("{:.2f}".format(totalTrueSlap/totalTesting*100)) + "%)"

  return dumResult, takResult, slapResult, accuracyResult


def tonePatternAutomaticIdentification(frameLength, hopLength, mfccCoefficient, k):
  cache.clear()

  baladiResult = []
  maqsumResult = []
  sayyidiResult = []
  totalTrueDum = 0
  totalTrueTak = 0
  accuracyResult = ""

  totalDum = 0
  totalTak = 0

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
    for tone in maqsumTonePattern:
      if tone == 'DUM':
        totalDum += 1
      elif tone == 'TAK':
        totalTak += 1
    for tone in sayyidiTonePattern:
      if tone == 'DUM':
        totalDum += 1
      elif tone == 'TAK':
        totalTak += 1

  for tonePattern in tonePatterns:
    for i in range(10):
      filename = 'D:/Ngoding/darbukaToneIdentification/static/dataset/tonePattern/' + tonePattern + '2_' + str(i+1) + '.wav'
      
      identification = []
      result = tonePatternIdentification(filename, k, frameLength, hopLength, mfccCoefficient, False)
      identification.append(result)

      if tonePattern == 'baladi' :
        resultDetect = []
        for i in range(5) :
          if result[i] == baladiTonePattern[i] :
            resultDetect.append('✅')
            if baladiTonePattern[i] == 'DUM' :
              totalTrueDum += 1
            elif baladiTonePattern[i] == 'TAK' :
              totalTrueTak += 1
          else :
            resultDetect.append('❌')
        identification.append(resultDetect)
        baladiResult.append(identification)
      elif tonePattern == 'maqsum' :
        resultDetect = []
        for i in range(5) :
          if result[i] == maqsumTonePattern[i] :
            resultDetect.append('✅')
            if maqsumTonePattern[i] == 'DUM' :
              totalTrueDum += 1
            elif maqsumTonePattern[i] == 'TAK' :
              totalTrueTak += 1
          else :
            resultDetect.append('❌')
        identification.append(resultDetect)
        maqsumResult.append(identification)
      if tonePattern == 'sayyidi' :
        resultDetect = []
        for i in range(5) :
          if result[i] == sayyidiTonePattern[i] :
            resultDetect.append('✅')
            if sayyidiTonePattern[i] == 'DUM' :
              totalTrueDum += 1
            elif sayyidiTonePattern[i] == 'TAK' :
              totalTrueTak += 1
          else :
            resultDetect.append('❌')
        identification.append(resultDetect)
        sayyidiResult.append(identification)

  accuracyResult += "Total = " + str(totalTrueDum + totalTrueTak) + "/" + str(totalDum + totalTak) + " (" + str("{:.2f}".format((totalTrueDum + totalTrueTak)/150*100)) + "%)<br/>"
  accuracyResult += "DUM Tone = " + str(totalTrueDum) + "/" + str(totalDum) + " (" + str("{:.2f}".format(totalTrueDum/totalDum*100)) + "%)<br/>"
  accuracyResult += "TAK Tone = " + str(totalTrueTak) + "/" + str(totalTak) + " (" + str("{:.2f}".format(totalTrueTak/totalTak*100)) + "%)<br/>"

  return baladiResult, maqsumResult, sayyidiResult, accuracyResult