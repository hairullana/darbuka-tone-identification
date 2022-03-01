from django.db import connection
from DataLatih.functions.mfccFunc import mfcc_extract
import numpy as np

def trainingData(windowLength, frameLength, mfccCoefficient):
  trainingResult = ""
  with connection.cursor() as cursor:

    # DELETE ALL DATA
    cursor.execute("DELETE FROM data_latih")
    connection.commit()
    cursor.execute("ALTER TABLE data_latih AUTO_INCREMENT = 0")
    connection.commit()

    def saveToDatabase(tone,mfcc):
      # QUERY AND PUSH
      cursor.execute("INSERT INTO data_latih(id, jenis_nada, ekstraksi) VALUES('','" + str(tone) + "','" + str(mfcc) + "')")
      connection.commit()
    
    # testing dataset
    toneType = ['dum','tak','slap']
    
    # TRAINING
    for i in toneType :
      for j in range(50) :
        filename = 'static/dataset/toneBasic/' + i + '/' + i + str(j+1) + '.wav'
        # EXTRACTION
        mfccResult = mfcc_extract(filename, windowLength, frameLength, mfccCoefficient)
        # MEAN OF EACH COEFFICIENT
        mfccResult = np.mean(mfccResult, axis=1)
        # CONVERT TO STRING
        mfccResult = np.array2string(mfccResult)
        # SAVE TO DB
        saveToDatabase(i, mfccResult)
      trainingResult += 'Successful training data on ' + i.upper() + ' tone.<br/>'

  return trainingResult