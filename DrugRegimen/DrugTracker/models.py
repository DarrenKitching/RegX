from django.db import models
from . import consts as c

# Create your models here.
class Perscription(models.Model):
	patient = models.CharField(max_length=c.MAX_NAME_LEN) # username of patient
	doctor = models.CharField(max_length=c.MAX_NAME_LEN) # username of doctor
	medicationCode = models.CharField(max_length=c.MAX_MEDCODE_LEN) # code to identify the medication
	medicationDose = models.IntegerField() # dosage to be taken
	doseUnit = models.CharField(max_length=c.MAX_UNIT_LEN) # unit of dosage
	timesPerDay = models.IntegerField()
	intervalBetweenDoses = models.IntegerField()
	perscriptionStartDate = models.DateField()
	totalNumberOfDoses = models.IntegerField()

class Medication(models.Model):
	medicationCode = models.CharField(max_length=c.MAX_MEDCODE_LEN) # key to identify medication
	medicationName = models.CharField(max_length=c.MAX_NAME_LEN) # name of the medication