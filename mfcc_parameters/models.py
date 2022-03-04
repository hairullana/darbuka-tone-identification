from django.db import models

# Create your models here.
class mfcc_parameters(models.Model):
  window_length = models.FloatField()
  frame_length = models.FloatField()
  mfcc_coefficient = models.IntegerField()

  class Meta:
    db_table = 'mfcc_parameters'