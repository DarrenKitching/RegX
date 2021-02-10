from django.db import models
from . import consts as c

# Create your models here.
class Perscription(models.Model):
	perscriptionID = models.CharField(max_length=c.MAX_PERSCRIPTION_ID_LEN) # unique perscription ID number
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

class MedConflict(models.Model):
	medication1Code = models.CharField(max_length=c.MAX_MEDCODE_LEN) # code to identify the medication
	medication2Code = models.CharField(max_length=c.MAX_MEDCODE_LEN) # code to identify the medication

class DoseURL(models.Model):
	doseURL = models.CharField(max_length=c.MAX_MEDCODE_LEN) # 10 digit url code unique to each dose assigned to a patient
	perscriptionID = models.CharField(max_length=c.MAX_PERSCRIPTION_ID_LEN) # identifies which perscription this URL is for
	doseNumber = models.IntegerField() # identifies which dose of the perscription this URL represents