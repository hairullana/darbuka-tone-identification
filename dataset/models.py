from django.db import models

class dataset(models.Model):
    tone = models.CharField(max_length=16)
    extraction = models.TextField()

    class Meta:
        managed = False
        db_table = 'dataset'
