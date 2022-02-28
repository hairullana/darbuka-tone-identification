from . import classificationFunc
from pydub import AudioSegment
import librosa

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

  hasilPresentaseKlasifikasi += "Total = " + str(jumlahKlasifikasiBenar) + "/60 (" + str(jumlahKlasifikasiBenar/60*100) + "%)"
  hasilPresentaseKlasifikasi += "DUM Tone = " + str(jumlahKlasifikasiDumBenar) + "/20 (" + str(jumlahKlasifikasiDumBenar/20*100) + "%)<br/>"
  hasilPresentaseKlasifikasi += "TAK Tone = " + str(jumlahKlasifikasiTakBenar) + "/20 (" + str(jumlahKlasifikasiTakBenar/20*100) + "%)<br/>"
  hasilPresentaseKlasifikasi += "SLAP Tone = " + str(jumlahKlasifikasiSlapBenar) + "/20 (" + str(jumlahKlasifikasiSlapBenar/20*100) + "%)<br/>"

  return hasilKlasifikasiDum, hasilKlasifikasiTak, hasilKlasifikasiSlap, hasilPresentaseKlasifikasi


def klasifikasiNadaDasar(windowLength, frameLength, mfccCoefficients, k):
  text = ['<br/>Klasifikasi Pola Nada Baladi (DD-T-D-T)<br/>', '<br/>Klasifikasi Pola Nada Maqsum (DT-T-D-T)<br/>', '<br/>Klasifikasi Pola Nada Sayyidi (DT-DD-T)<br/>']
  for n in range(3):
    for i in range(10):
      text[n] += '<br/>'
      if n == 0 :
        filename = 'd:/ngoding/sistem darbuka/dataset/tonePattern/baladi2_' + str(i+1) + '.wav'
      elif n == 1 :
        filename = 'd:/ngoding/sistem darbuka/dataset/tonePattern/maqsum2_' + str(i+1) + '.wav'
      else :
        filename = 'd:/ngoding/sistem darbuka/dataset/tonePattern/sayyidi2_' + str(i+1) + '.wav'


      x, sr = librosa.load(filename)
      # x, index = librosa.effects.trim(x, top_db=30)
      onsetDetection = librosa.onset.onset_detect(x, sr=sr, units='time')

      BaladiTonePattern = ['dum', 'dum', 'tak', 'dum', 'tak']
      i=0
      for onset in onsetDetection:
          newAudio = AudioSegment.from_wav(filename)
          start = int(onsetDetection[i]*1000)
          if i != len(onsetDetection)-1 :
              end = int(onsetDetection[i+1]*1000)
          else :
              end = int(librosa.get_duration(filename=filename)*1000)
          newAudio = newAudio[start:end]
          newAudio.export('temp.wav', format="wav")
          hasil, k_dum, k_tak, k_slap, indeks = classificationFunc.klasifikasi('temp.wav', k, windowLength, frameLength, mfccCoefficients)
          i += 1
          text[n] += hasil + ' - '
  
  return text