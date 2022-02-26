from . import classificationFunc

def klasifikasiNada(windowLength, frameLength, mfccCoefficients, k):

  hasilKlasifikasiDum = ""
  hasilKlasifikasiTak = ""
  hasilKlasifikasiSlap = ""
  jumlahKlasifikasiDumBenar = 0
  jumlahKlasifikasiTakBenar = 0
  jumlahKlasifikasiSlapBenar = 0
  hasilPresentaseKlasifikasi = ""

  # TESTING DUM
  hasilKlasifikasiDum += '<br/>Sedang melakukan klasifikasi nada DUM (K=' + str(k) + ')<br/>'
  for i in range(20) :
    indeks = i + 51
    filename = 'static/dataset/toneBasic/dum/dum' + str(indeks) + '.wav'
    hasil, k_dum, k_tak, k_slap, indeks = classificationFunc.klasifikasi(filename, k, windowLength, frameLength, mfccCoefficients)
    file = filename.split(sep="/")
    file2 = file[len(file)-1]
    if hasil == 'DUM':
      jumlahKlasifikasiDumBenar += 1
    hasilKlasifikasiDum += '<br/>Hasil dari klasifikasi ' + file2 + ' adalah nada ' + hasil

  # TESTING TAK
  hasilKlasifikasiTak += '<br/>Sedang melakukan klasifikasi nada TAK (K=' + str(k) + ')<br/>'
  for i in range(20) :
    indeks = i + 51
    filename = 'static/dataset/toneBasic/tak/tak' + str(indeks) + '.wav'
    hasil, k_dum, k_tak, k_slap, indeks = classificationFunc.klasifikasi(filename, k, windowLength, frameLength, mfccCoefficients)
    file = filename.split(sep="/")
    file2 = file[len(file)-1]
    if hasil == 'TAK':
      jumlahKlasifikasiTakBenar += 1
    hasilKlasifikasiTak += '<br/>Hasil dari klasifikasi ' + file2 + ' adalah nada ' + hasil

  # TESTING SLAP
  hasilKlasifikasiSlap += '<br/>Sedang melakukan klasifikasi nada SLAP (K=' + str(k) + ')<br/>'
  for i in range(20) :
    indeks = i + 51
    filename = 'static/dataset/toneBasic/slap/slap' + str(indeks) + '.wav'
    hasil, k_dum, k_tak, k_slap, indeks = classificationFunc.klasifikasi(filename, k, windowLength, frameLength, mfccCoefficients)
    file = filename.split(sep="/")
    file2 = file[len(file)-1]
    if hasil == 'SLAP':
      jumlahKlasifikasiSlapBenar += 1
    hasilKlasifikasiSlap += '<br/>Hasil dari klasifikasi ' + file2 + ' adalah nada' + hasil
  
  jumlahKlasifikasiBenar = jumlahKlasifikasiDumBenar + jumlahKlasifikasiTakBenar + jumlahKlasifikasiSlapBenar

  hasilPresentaseKlasifikasi += "Akurasi Nada DUM = " + str(jumlahKlasifikasiDumBenar) + "/20 (" + str(jumlahKlasifikasiDumBenar/20*100) + "%)<br/>"
  hasilPresentaseKlasifikasi += "Akurasi Nada TAK = " + str(jumlahKlasifikasiTakBenar) + "/20 (" + str(jumlahKlasifikasiTakBenar/20*100) + "%)<br/>"
  hasilPresentaseKlasifikasi += "Akurasi Nada SLAP = " + str(jumlahKlasifikasiSlapBenar) + "/20 (" + str(jumlahKlasifikasiSlapBenar/20*100) + "%)<br/>"
  hasilPresentaseKlasifikasi += "Akurasi Sistem = " + str(jumlahKlasifikasiBenar) + "/60 (" + str(jumlahKlasifikasiBenar/60*100) + "%)"

  return hasilKlasifikasiDum, hasilKlasifikasiTak, hasilKlasifikasiSlap, hasilPresentaseKlasifikasi