from tkinter import filedialog as fd
import classificationFunc

# open button
def select_file(k, windowLength, frameLength, mfccCoefficients, klasifikasiDum, klasifikasiTak, klasifikasiSlap, presentaseKlasifikasi, info):
  filetypes = (
    ('wav files', '*.wav'),
    ('All files', '*.*')
  )

  filename = fd.askopenfilename(
    title='Pilih Nada',
    initialdir='D:/Ngoding/Sistem Darbuka/DataTA/Nada Dasar/',
    filetypes=filetypes)

  hasil, k_dum, k_tak, k_slap, indeks = classificationFunc.klasifikasi(filename, k, windowLength, frameLength, mfccCoefficients)
  file = filename.split(sep="/")
  file2 = file[len(file)-1]

  klasifikasiDum.config(text="")
  klasifikasiTak.config(text="")
  klasifikasiSlap.config(text="")
  presentaseKlasifikasi.config(text="")
  info.config(text='\nHasil dari klasifikasi ' + file2 + ' adalah nada ' + hasil)