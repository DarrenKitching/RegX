from django.db import models

# Create your models here.
class Perscription(models.Model):
	patient = models.CharField(max_length=50) # username of patient
	doctor = models.CharField(max_length=50) # username of doctor
	medicationCode = models.CharField(max_length=50) # code to identify the medication
	medicationDose = models.CharField(max_length=50) # dosage to be taken
	timesPerDay = models.IntegerField()
	intervalBetweenDoses = models.IntegerField()
	perscriptionStartDate = models.DateField()
	totalNumberOfDoses = models.IntegerField()

class Medication(models.Model):
	medicationCode = models.CharField(max_length=50) # key to identify medication
	medicationName = models.CharField(max_length=50) # name of the medication