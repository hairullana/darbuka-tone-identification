from django.db import models

class DataLatih(models.Model):
    jenis_nada = models.CharField(max_length=16)
    ekstraksi = models.TextField()

    class Meta:
        managed = False
        db_table = 'data_latih'
