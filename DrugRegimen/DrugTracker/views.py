from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import DrugConflictSerializer, DrugNotesSerializer
import datetime
from datetime import date
from . import models
from . import qrcodes
import random
import string

def index(request):
	"""
	This function is run when the user opens the site at http://127.0.0.1:8000

	This function will display login.html in the user's web browser.

	Args:
		request (request): Request is built in to django and stores the current state of the system e.g. the username of the logged in user.

	Returns:
		render: Will render the login.html file.
	"""
	# print(generateTenDigtURL())
	return render(request, 'login.html')

def home(request):
	"""
	This function is run when the user has logged in and gets brought to http://127.0.0.1:8000/home

	The function will check if the logged in user is a patient, pharmacist or doctor and will return the appropiate home screen accordingly.

	Args:
		request (request): Request is built in to django and stores the current state of the system e.g. the username of the logged in user.

	Returns:
		render: Return will render either patientHome, pharmacistHome or doctorHome function depending on the type of user logged in. 

	"""
	allPatients = models.PatientGroup.objects.all()
	for patient in allPatients:
		if patient.patientUsername == request.user.username: # check to see if logged in user is a patient
			return patientHome(request) # if they are then call patientHome
	allPharmacists = models.PharmacistGroup.objects.all()
	for pharmacist in allPharmacists:
		if pharmacist.pharmacistUsername == request.user.username: # check to see if logged in user is a pharmacist account
			return pharmacistHome(request) # if they are then call pharmacistHome
	allDoctors = models.DoctorGroup.objects.all()
	for doctor in allDoctors:
		if doctor.doctorUsername == request.user.username: # check to see if logged in user is a doctor
			return doctorHome(request) # if they are then call doctorHome
	return HttpResponse("Error: Your account isn't associated with any user group") # this line is only run if the logged in user isn't assigned to any group

def getMedicationName(medicationCode):
	"""
	This function is used to get the name of a medication using its unique medication code.

	This function is the link between the unique key for a medication (its code) and how to get its name from that.

	Args:
		request (request): Request is built in to django and stores the current state of the system e.g. the username of the logged in user.

	Returns:
		string: Will return a string of the name of the medication with that code or a blank screen if there is no medication with that code.

	"""
	allMedications = models.Medication.objects.all()
	for medication in allMedications:
		if medicationCode == medication.medicationCode:
			return medication.medicationName
	return "" # no medication with that code has been found

def takeDose(request, doseURL): # extract dose id from URL
	"""
	This function is called when the user navigates to http://127.0.0.1:8000/dose/<somenumber>

	Our QRCodes will open up to unique dose sites, e.g. http://127.0.0.1:8000/dose/1z5Lff10AN
	When these links are opened this function will be called. We can then check that the logged in user owns the dose associated with this dose URL
	and later on implement the record video feature at this page.

	Args:
		request (request): Request is built in to django and stores the current state of the system e.g. the username of the logged in user.
		doseURL (string): doseURL is a string of what comes after /dose/ in the url opened. For example if the user opened
		http://127.0.0.1:8000/dose/1z5Lff10AN then doseURL would be equal to 1z5Lff10AN when this function is called.

	Returns:
		render: Currently the function is only returning some Text showing the doseURL the function has been called with.

	"""
	return HttpResponse("Test " + doseURL)

def patientHome(request):
	"""
	This function is run when the user has logged into a patient account and gets brought to http://127.0.0.1:8000/home

	This function will display patienthome.html in the user's web browser. It will pass in a list of prescriptions which the user needs to 
	take today into home.html

	Args:
		request (request): Request is built in to django and stores the current state of the system e.g. the username of the logged in user.

	Returns:
		render: Will render the patienthome.html file with the list of the user's prescriptions that need to be taken today.

	"""
	# url = 'http://uca.edu' # testing QRcode generation - delete later
	# qrcodes.createQR(url) # testing QRcode generation - delete later
	allPrescriptions = models.Prescription.objects.all()
	patientPrescriptions = []
	for prescription in allPrescriptions:
		if prescription.patientId == request.user.username:
			patientPrescriptions.append(prescription)
	patientItems = getAllPrescriptionItems(patientPrescriptions)
	todaysItems = getTodaysItems(patientItems)
	context = {
		'medications': todaysItems,
		}
	return render(request, 'patienthome.html', context)

def pharmacistHome(request):
	"""
	This function is run when the user has logged into a pharmacist account and gets brought to http://127.0.0.1:8000/home

	This function will display pharmacisthome.html in the user's web browser.

	Args:
		request (request): Request is built in to django and stores the current state of the system e.g. the username of the logged in user.

	Returns:
		render: Will render the pharmacisthome.html file.

	"""
	return render(request, 'pharmacisthome.html')

def doctorHome(request):
	"""
	This function is run when the user has logged into a doctor account and gets brought to http://127.0.0.1:8000/home

	This function will display doctorhome.html in the user's web browser.

	Args:
		request (request): Request is built in to django and stores the current state of the system e.g. the username of the logged in user.

	Returns:
		render: Will render the doctorhome.html file.
	"""
	patients = ['test', 'test', 'test']
	context = {'patients' : patients}
	# patientNames = []
	# patientDrugs = [['']]
	# patientLastDose [['']]?
	return render(request, 'doctorhome.html', context)

def generateTenDigtURL():
	"""
	This function generates a unique 10 digit code that can be used to build a unique URL for qrcodes to point to.

	This function creates a 10 digit combination of upper case and lower case characters as well as digits. It will then check that this combination
	has not already been used for another dose. If it has been used before then it will generate a new url otherwise it will return the one it has made.

	Args:

	Returns:
		string: A string of length 10 will be returned containing a unique combination to be used for a dose URL.

	"""
	newUrl = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
	allDoses = models.DoseURL.objects.all()
	for dose in allDoses:
		if dose.doseURL == newUrl: # check for rare conflict when a generated dose URL has already been used for a different dose.
			return generateTenDigtURL()
	return newUrl

def getPrescriptionItems(prescription):
	items = []
	PrescriptionItems = models.PrescriptionItem.objects.all()
	for prescriptionItem in PrescriptionItems:
		if prescriptionItem.prescription == prescription:
			items.append(prescriptionItem.item)
	return items

def getAllPrescriptionItems(patientPrescriptions):
	items = []
	allPrescriptionItems = models.PrescriptionItem.objects.all()
	for patientPrescription in patientPrescriptions:
		for prescriptionItem in allPrescriptionItems:
			if prescriptionItem.prescription == patientPrescription:
				items.append(prescriptionItem.item)
	return items

def getTodaysItems(items):
	todaysItems = []
	now = datetime.datetime.now()
	today = date.today()
	for item in items:
		if item.durationUnit == 'years':
			if abs(today - item.startDate).days <= (item.durationValue * 365):
				todaysItems.append(item)
		if item.durationUnit == 'months':
			if abs(today - item.startDate).days <= (item.durationValue * 365):
				todaysItems.append(item)
		else: # assume years
			if abs(today - item.startDate).days <= (item.durationValue * 365):
				todaysItems.append(item)
	return todaysItems


class DrugConflictViewSet (viewsets.ModelViewSet):
	queryset = models.DrugConflict.objects.all()
	serializer_class = DrugConflictSerializer

class DrugNotesViewSet (viewsets.ModelViewSet):
	queryset = models.DrugNotes.objects.all()
	serializer_class = DrugNotesSerializer