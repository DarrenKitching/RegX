from django.db import models
from . import consts as c

class DrugConflict(models.Model):
	drug1 = models.CharField(max_length=50)
	drug2 = models.CharField(max_length=50)
	conflictSeverity = models.CharField(max_length=50)
	conflictNotes = models.CharField(max_length=50)

class DrugNotes(models.Model):
	drug = models.CharField(max_length=50)
	notes = models.CharField(max_length=5000)

class PatientGroup(models.Model):
	patientUsername = models.CharField(max_length=c.MAX_NAME_LEN) # username of patient

class PharmacistGroup(models.Model):
	pharmacistUsername = models.CharField(max_length=c.MAX_NAME_LEN) # username of pharmacist account

class DoctorGroup(models.Model):
	doctorUsername = models.CharField(max_length=c.MAX_NAME_LEN) # username of doctor's account

class Item(models.Model):
	dosageForm = models.CharField(max_length=50)
	doseValue = models.IntegerField() # e.g. if you need to take two tablets of the same drug a day you'd have one video for doseCount 1 and another for doseCount 2
	doseUnit = models.CharField(max_length=10)
	drug = models.CharField(max_length=50)
	durationValue = models.IntegerField()
	durationUnit = models.CharField(max_length=50)
	frequency = models.CharField(max_length=50)
	route = models.CharField(max_length=50)
	quantity = models.CharField(max_length=50)
	status = models.CharField(max_length=50)
	startDate = models.DateField(null=True) # when the prescription has been started
	videoRequired = models.BooleanField()
	videoURL = models.CharField(max_length=10) # unique ten digit url for uploading the video

class Prescription(models.Model):
	comment = models.CharField(max_length=50)
	dateDispensed = models.CharField(max_length=50, null=True, blank=True)
	dateIssued = models.CharField(max_length=50)
	dateReceived = models.CharField(max_length=50, null=True, blank=True)
	dispensed = models.BooleanField()
	doctorId = models.CharField(max_length=50)
	patientId = models.CharField(max_length=50)
	pharmacyId = models.CharField(max_length=50)
	pharmacyNote = models.CharField(max_length=500, null=True, blank=True)

class PrescriptionItem(models.Model):
	prescription = models.ForeignKey('Prescription', on_delete=models.CASCADE)
	item = models.ForeignKey('Item', on_delete=models.CASCADE)

class DoctorPatient(models.Model):
	doctorUsername = models.CharField(max_length=c.MAX_NAME_LEN)
	patientUsername = models.CharField(max_length=c.MAX_NAME_LEN) # username of patient
	relationshipConfirmed = models.BooleanField()

class DoseURL(models.Model):
	doseURL = models.CharField(max_length = 10)

class PrescriptionCollector(models.Model):
	patientUsername = models.CharField(max_length=c.MAX_NAME_LEN) # username of patient
	collectorName = models.CharField(max_length=c.MAX_NAME_LEN) # name of person allowed to collect on patient's behalf

class PatientPharmacy(models.Model):
	patientUsername = models.CharField(max_length=c.MAX_NAME_LEN) # username of patient
	pharmacyId = models.CharField(max_length=50)

class PatientGMS(models.Model):
	patientUsername = models.CharField(max_length=c.MAX_NAME_LEN) # username of patient
	gms = models.CharField(max_length=50) # gms number