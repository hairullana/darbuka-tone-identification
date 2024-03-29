from django.db import connection
from .mfccFunc import mfcc_extract
import numpy as np
from mfcc_parameters.models import mfcc_parameters

def trainingData(frameLength, overlap, mfccCoefficient):
  trainingResult = ""

  mfccParameter = mfcc_parameters.objects.all()[0]
  mfccParameter.frame_length = frameLength
  mfccParameter.overlap = overlap
  mfccParameter.mfcc_coefficient = mfccCoefficient
  mfccParameter.save()

  with connection.cursor() as cursor:

    # DELETE ALL DATA
    cursor.execute("DELETE FROM dataset")
    connection.commit()
    cursor.execute("ALTER TABLE dataset AUTO_INCREMENT = 0")
    connection.commit()

    def saveToDatabase(tone,mfcc):
      # QUERY AND PUSH
      cursor.execute("INSERT INTO dataset(id, tone, extraction) VALUES('','" + str(tone) + "','" + str(mfcc) + "')")
      connection.commit()
    
    # testing dataset
    toneType = ['dum','tak','slap']
    
    # TRAINING
    for i in toneType :
      for j in range(50) :
        filename = 'C:/Coding/darbukaToneIdentification/static/dataset/toneBasic/train/' + i + '/' + i + str(j+1) + '.wav'
        # EXTRACTION
        mfccResult = mfcc_extract(filename, frameLength, overlap, mfccCoefficient)
        # CONVERT TO STRING
        mfccResult = np.array2string(mfccResult)
        # SAVE TO DB
        saveToDatabase(i, mfccResult)
      trainingResult += 'Successful training 50 data on ' + i.upper() + ' tone.<br/>'

  return trainingResult