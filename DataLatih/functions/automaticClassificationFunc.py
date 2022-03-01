from . import classificationFunc
from pydub import AudioSegment
import librosa
import os

def klasifikasiNada(windowLength, frameLength, mfccCoefficients, k):

  hasilKlasifikasiDum = []
  hasilKlasifikasiTak = []
  hasilKlasifikasiSlap = []
  jumlahKlasifikasiDumBenar = 0
  jumlahKlasifikasiTakBenar = 0
  jumlahKlasifikasiSlapBenar = 0
  hasilPresentaseKlasifikasi = ""

  # TESTING DUM
  for i in range(20) :
    indeks = i + 51
    filename = 'static/dataset/toneBasic/dum/dum' + str(indeks) + '.wav'
    hasil, k_dum, k_tak, k_slap, indeks = classificationFunc.klasifikasi(filename, k, windowLength, frameLength, mfccCoefficients)
    file = filename.split(sep="/")
    file2 = file[len(file)-1]
    if hasil == 'DUM':
      jumlahKlasifikasiDumBenar += 1
    hasilKlasifikasiDum.append(hasil)

  # TESTING TAK
  for i in range(20) :
    indeks = i + 51
    filename = 'static/dataset/toneBasic/tak/tak' + str(indeks) + '.wav'
    hasil, k_dum, k_tak, k_slap, indeks = classificationFunc.klasifikasi(filename, k, windowLength, frameLength, mfccCoefficients)
    file = filename.split(sep="/")
    file2 = file[len(file)-1]
    if hasil == 'TAK':
      jumlahKlasifikasiTakBenar += 1
    hasilKlasifikasiTak.append(hasil)

  # TESTING SLAP
  for i in range(20) :
    indeks = i + 51
    filename = 'static/dataset/toneBasic/slap/slap' + str(indeks) + '.wav'
    hasil, k_dum, k_tak, k_slap, indeks = classificationFunc.klasifikasi(filename, k, windowLength, frameLength, mfccCoefficients)
    file = filename.split(sep="/")
    file2 = file[len(file)-1]
    if hasil == 'SLAP':
      jumlahKlasifikasiSlapBenar += 1
    hasilKlasifikasiSlap.append(hasil)
  
  jumlahKlasifikasiBenar = jumlahKlasifikasiDumBenar + jumlahKlasifikasiTakBenar + jumlahKlasifikasiSlapBenar

  hasilPresentaseKlasifikasi += "Total = " + str(jumlahKlasifikasiBenar) + "/60 (" + str("{:.2f}".format(jumlahKlasifikasiBenar/60*100)) + "%)<br/>"
  hasilPresentaseKlasifikasi += "DUM Tone = " + str(jumlahKlasifikasiDumBenar) + "/20 (" + str("{:.2f}".format(jumlahKlasifikasiDumBenar/20*100)) + "%)<br/>"
  hasilPresentaseKlasifikasi += "TAK Tone = " + str(jumlahKlasifikasiTakBenar) + "/20 (" + str("{:.2f}".format(jumlahKlasifikasiTakBenar/20*100)) + "%)<br/>"
  hasilPresentaseKlasifikasi += "SLAP Tone = " + str(jumlahKlasifikasiSlapBenar) + "/20 (" + str("{:.2f}".format(jumlahKlasifikasiSlapBenar/20*100)) + "%)"

  return hasilKlasifikasiDum, hasilKlasifikasiTak, hasilKlasifikasiSlap, hasilPresentaseKlasifikasi


def klasifikasiNadaDasar(windowLength, frameLength, mfccCoefficients, k):
  hasilKlasifikasiBaladi = []
  hasilKlasifikasiMaqsum = []
  hasilKlasifikasiSayyidi = []
  jumlahKlasifikasiDumBenar = 0
  jumlahKlasifikasiTakBenar = 0
  jumlahKlasifikasiSlapBenar = 0
  hasilPresentaseKlasifikasi = ""

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
        hasil, k_dum, k_tak, k_slap, indeks = classificationFunc.klasifikasi('temp.wav', k, windowLength, frameLength, mfccCoefficients)
        if j != len(onsetDetection):
          temp += hasil.lower() + '-'
        else :
          temp += hasil.lower()
        
        if j <= 5 :
          if tonePattern == 'baladi' :
            if hasil == baladiTonePattern[j-1] :
              toneDetect.append(True)
              if hasil == 'DUM' :
                jumlahKlasifikasiDumBenar += 1
              elif hasil == 'TAK' :
                jumlahKlasifikasiTakBenar += 1
              elif hasil == 'SLAP' :
                jumlahKlasifikasiSlapBenar += 1
            else :
              toneDetect.append(False)
          elif tonePattern == 'maqsum' :
            if hasil == maqsumTonePattern[j-1] :
              toneDetect.append(True)
              if hasil == 'DUM' :
                jumlahKlasifikasiDumBenar += 1
              elif hasil == 'TAK' :
                jumlahKlasifikasiTakBenar += 1
              elif hasil == 'SLAP' :
                jumlahKlasifikasiSlapBenar += 1
            else :
              toneDetect.append(False)
          elif tonePattern == 'sayyidi' :
            if hasil == sayyidiTonePattern[j-1] :
              toneDetect.append(True)
              if hasil == 'DUM' :
                jumlahKlasifikasiDumBenar += 1
              elif hasil == 'TAK' :
                jumlahKlasifikasiTakBenar += 1
              elif hasil == 'SLAP' :
                jumlahKlasifikasiSlapBenar += 1
            else :
              toneDetect.append(False)
        else :
          toneDetect.append(False)
      
        j += 1

      resultDetect.append(temp)
      resultDetect.append(toneDetect)

      if tonePattern == 'baladi' :
        hasilKlasifikasiBaladi.append(resultDetect)
      elif tonePattern == 'maqsum' :
        hasilKlasifikasiMaqsum.append(resultDetect)
      elif tonePattern == 'sayyidi' :
        hasilKlasifikasiSayyidi.append(resultDetect)
      
      
  os.remove('temp.wav')

  hasilPresentaseKlasifikasi += "Total = " + str(jumlahKlasifikasiDumBenar + jumlahKlasifikasiTakBenar + jumlahKlasifikasiSlapBenar) + "/" + str(totalDum + totalTak + totalSlap) + " (" + str("{:.2f}".format((jumlahKlasifikasiDumBenar + jumlahKlasifikasiTakBenar + jumlahKlasifikasiSlapBenar)/150*100)) + "%)<br/>"
  hasilPresentaseKlasifikasi += "DUM Tone = " + str(jumlahKlasifikasiDumBenar) + "/" + str(totalDum) + " (" + str("{:.2f}".format(jumlahKlasifikasiDumBenar/totalDum*100)) + "%)<br/>"
  hasilPresentaseKlasifikasi += "TAK Tone = " + str(jumlahKlasifikasiTakBenar) + "/" + str(totalTak) + " (" + str("{:.2f}".format(jumlahKlasifikasiTakBenar/totalTak*100)) + "%)<br/>"
  if totalSlap != 0:
    hasilPresentaseKlasifikasi += "SLAP Tone = " + str(jumlahKlasifikasiSlapBenar) + "/" + str(totalSlap) + " (" + str("{:.2f}".format(jumlahKlasifikasiSlapBenar/totalSlap*100)) + "%)"

  return hasilKlasifikasiBaladi, hasilKlasifikasiMaqsum, hasilKlasifikasiSayyidi, hasilPresentaseKlasifikasi