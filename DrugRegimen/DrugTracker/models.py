from django.db import models
from . import consts as c

# Create your models here.
class Medication(models.Model):
	medicationCode = models.CharField(max_length=c.MAX_MEDCODE_LEN) # key to identify medication
	medicationName = models.CharField(max_length=c.MAX_NAME_LEN) # name of the medication
	medicationNotes = models.CharField(max_length=c.MAX_MED_NOTES_LEN) # any notes about the medication e.g. take with food

class MedConflict(models.Model):
	medication1Code = models.CharField(max_length=c.MAX_MEDCODE_LEN) # code to identify the medication
	medication2Code = models.CharField(max_length=c.MAX_MEDCODE_LEN) # code to identify the medication
	conflictDetails = models.CharField(max_length=c.MAX_CONFLICT_DETAILS_LEN) # details of the conflict
	conflictSeverity = models.CharField(max_length=c.MAX_SEVERITY_LEN) # severity of the conflict

class DoseURL(models.Model):
	doseURL = models.CharField(max_length=c.MAX_MEDCODE_LEN) # 10 digit url code unique to each dose assigned to a patient
	prescriptionID = models.CharField(max_length=c.MAX_PRESCRIPTION_ID_LEN) # identifies which prescription this URL is for
	doseNumber = models.IntegerField() # identifies which dose of the prescription this URL represents

class PatientGroup(models.Model):
	patientUsername = models.CharField(max_length=c.MAX_NAME_LEN) # username of patient

class PharmacistGroup(models.Model):
	pharmacistUsername = models.CharField(max_length=c.MAX_NAME_LEN) # username of pharmacist account

class DoctorGroup(models.Model):
	doctorUsername = models.CharField(max_length=c.MAX_NAME_LEN) # username of doctor's account

class Item(models.Model):
	dosageForm = models.CharField(max_length=50)
	doseValue = models.IntegerField()
	doseUnit = models.CharField(max_length=10)
	drug = models.CharField(max_length=50)
	durationValue = models.IntegerField()
	durationUnit = models.CharField(max_length=50)
	frequency = models.CharField(max_length=50)
	route = models.CharField(max_length=50)
	quantity = models.CharField(max_length=50)
	status = models.CharField(max_length=50)

class Prescription(models.Model):
	comment = models.CharField(max_length=50)
	dateDispensed = models.CharField(max_length=50)
	dateIssued = models.CharField(max_length=50)
	dateReceived = models.CharField(max_length=50)
	dispensed = models.BooleanField()
	doctorId = models.CharField(max_length=50)
	patientId = models.CharField(max_length=50)
	pharmacyId = models.CharField(max_length=50)
	pharmacyNote = models.CharField(max_length=500)

class PrescriptionItem(models.Model):
	prescription = models.ForeignKey('Prescription', on_delete=models.CASCADE)
	item = models.ForeignKey('Item', on_delete=models.CASCADE)


