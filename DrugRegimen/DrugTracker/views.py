from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import DrugConflictSerializer, DrugNotesSerializer
from django.views.decorators.csrf import csrf_exempt
import datetime
from datetime import date
from . import models
from . import motionTracking
from . import qrcodes
import random
import string
import re
from itertools import zip_longest
from . import rxnavAPI
from . import createUser
import threading
import os.path

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
	return render(request, 'login/login.html')

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

def register(request):
	return render(request, 'login/register.html') 

def newAccount(request):
	firstName = request.POST.get('first-name')
	secondName = request.POST.get('second-name')
	username = request.POST.get('username')
	email = request.POST.get('email')
	password = request.POST.get('password')
	passwordRepeat = request.POST.get('password-repeat')
	if password == passwordRepeat:
		createUser.createNewUser(username, password)
	return render(request, 'login/login.html')


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
	now = datetime.datetime.now()
	today = date.today()
	context = {
		'doseURL': doseURL,
		'date': str(today)
	}
	return render(request, 'recordvideo/recordvideo.html', context)

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
		'username': re.sub(r"(\w)([A-Z])", r"\1 \2", request.user.username),
		}
	return render(request, 'home/patienthome.html', context)

def pharmacistHome(request):
	"""
	This function is run when the user has logged into a pharmacist account and gets brought to http://127.0.0.1:8000/home

	This function will display pharmacisthome.html in the user's web browser.

	Args:
		request (request): Request is built in to django and stores the current state of the system e.g. the username of the logged in user.

	Returns:
		render: Will render the pharmacisthome.html file.

	"""
	pharmacyPrescriptions = []
	allPrescriptions = models.Prescription.objects.all()
	for prescription in allPrescriptions:
		if prescription.pharmacyId == request.user.username:
			pharmacyPrescriptions.append(prescription)
	notDispensed = []
	dispensedNotReceived = []
	dispensedAndReceived = []
	notDispensedIds = []
	dispensedNotReceivedIds = []
	notDispensedCollectors = []
	dispensedNotReceivedCollectors = []
	for prescription in pharmacyPrescriptions:
		if prescription.dispensed == False:
			notDispensed.append(prescription)
			notDispensedIds.append(prescription.id)
			notDispensedCollectors.append(getCollectors(prescription.patientId))
		elif prescription.dateReceived is None:
			dispensedNotReceived.append(prescription)
			dispensedNotReceivedIds.append(prescription.id)
			dispensedNotReceivedCollectors.append(getCollectors(prescription.patientId))
		else:
			dispensedAndReceived.append(prescription)
	notDispensedPresciptionItems = []
	dispensedNotReceivedPrescriptionItems = []
	dispensedAndReceivedPrescriptionItems = []
	for prescription in notDispensed:
		notDispensedPresciptionItems.append(getPrescriptionItems(prescription))
	for prescription in dispensedNotReceived:
		dispensedNotReceivedPrescriptionItems.append(getPrescriptionItems(prescription))
	for prescription in dispensedAndReceived:
		dispensedAndReceivedPrescriptionItems.append(getPrescriptionItems(prescription))
	context = {
		'username': re.sub(r"(\w)([A-Z])", r"\1 \2", request.user.username),
		'notDispensed': zip(notDispensed, notDispensedPresciptionItems, notDispensedIds, notDispensedCollectors),
		'dispensedNotReceived': zip(dispensedNotReceived, dispensedNotReceivedPrescriptionItems, dispensedNotReceivedIds, dispensedNotReceivedCollectors),
	}
	return render(request, 'home/pharmacisthome.html', context)

def doctorHome(request):
	"""
	This function is run when the user has logged into a doctor account and gets brought to http://127.0.0.1:8000/home

	This function will display doctorhome.html in the user's web browser.

	Args:
		request (request): Request is built in to django and stores the current state of the system e.g. the username of the logged in user.

	Returns:
		render: Will render the doctorhome.html file.
	"""
	allDoctorPatientAssignmentsDoctorPatient = models.DoctorPatient.objects.all()
	patients = [] # pateints assigned to this doctor
	for doctorPatientRelationship in allDoctorPatientAssignmentsDoctorPatient:
		if doctorPatientRelationship.doctorUsername == request.user.username:
			patients.append(doctorPatientRelationship.patientUsername)
	allPrescriptions = models.Prescription.objects.all()
	patientDrugs = [] # a list of drugs to be taken by this doctor's patients today
	patientAssignedToDrug = []
	confidenceScores = []
	for patient in patients:
		for prescription in allPrescriptions:
			if prescription.patientId == patient:
				patientItems = getAllPrescriptionItems([prescription]) # get this patient's prescriptions
				todaysItems = getTodaysItems(patientItems) # get a list of items this patient needs to take today
				for item in todaysItems:
					patientDrugs.append(item)
					path = 'media/recorded-videos/' + item.videoURL + ('_' + (str(date.today()))) + '.webm'
					confidenceScores.append(motionTracking.obtainConfidenceScore(path))
				for item in todaysItems:
					patientAssignedToDrug.append(prescription.patientId)
	zipped = zip(patientAssignedToDrug, patientDrugs, confidenceScores)
	context = {
		'patientsAndDrugs' : zipped,
		'username' : 'Dr. ' + re.sub(r"(\w)([A-Z])", r"\1 \2", request.user.username),
		'date': str(date.today()),
		'confidenceScores' : confidenceScores
		}
	return render(request, 'home/doctorhome.html', context)

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
	newDoseURL = models.DoseURL(doseURL = newUrl)
	newDoseURL.save()
	return newUrl

def getPrescriptionItems(prescription):
	items = []
	PrescriptionItems = models.PrescriptionItem.objects.all()
	for prescriptionItem in PrescriptionItems:
		if prescriptionItem.prescription == prescription:
			# print(str(prescriptionItem.prescription) + " " + str(prescription))
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
		if item.startDate is not None:
			if item.durationUnit == 'Years':
				if abs(today - item.startDate).days <= (item.durationValue * 365):
					todaysItems.append(item)
			if item.durationUnit == 'Months':
				if abs(today - item.startDate).days <= (item.durationValue * 30):
					todaysItems.append(item)
			if item.durationUnit == 'Weeks':
				if abs(today - item.startDate).days <= (item.durationValue * 7):
					todaysItems.append(item)
			else: # assume days
				if abs(today - item.startDate).days <= (item.durationValue):
					todaysItems.append(item)
		else:
			item.startDate = date.today()
			item.save()
			todaysItems.append(item)
	return todaysItems


class DrugConflictViewSet (viewsets.ModelViewSet):
	queryset = models.DrugConflict.objects.all()
	serializer_class = DrugConflictSerializer

class DrugNotesViewSet (viewsets.ModelViewSet):
	queryset = models.DrugNotes.objects.all()
	serializer_class = DrugNotesSerializer

@csrf_exempt
def upload(request):
	BASE = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

	if request.is_ajax():
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			path = os.path.join(BASE, 'media/recorded-videos/' + request.POST.get('doseURL') + ('_' + request.POST.get('date')) + '.webm')
			print("valid")
			with open(path, 'wb+') as destination:
				for chunk in request.FILES['video'].chunks():
					destination.write(chunk)
		else:
			print("invalid")
	return patientHome(request)

def about(request):
	allPatients = models.PatientGroup.objects.all()
	for patient in allPatients:
		if patient.patientUsername == request.user.username: # check to see if logged in user is a patient
			return patientAbout(request) # if they are then call patientAbout
	allPharmacists = models.PharmacistGroup.objects.all()
	for pharmacist in allPharmacists:
		if pharmacist.pharmacistUsername == request.user.username: # check to see if logged in user is a pharmacist account
			return pharmacistAbout(request) # if they are then call pharmacistAbout
	allDoctors = models.DoctorGroup.objects.all()
	for doctor in allDoctors:
		if doctor.doctorUsername == request.user.username: # check to see if logged in user is a doctor
			return doctorAbout(request) # if they are then call doctorAbout
	return HttpResponse("Error: Your account isn't associated with any user group") # this line is only run if the logged in user isn't assigned to any group

def patientAbout(request):
	context = {
		'username': re.sub(r"(\w)([A-Z])", r"\1 \2", request.user.username),
	}
	return render(request, 'about/patientabout.html', context)

def doctorAbout(request):
	context = {
		'username': 'Dr. ' + re.sub(r"(\w)([A-Z])", r"\1 \2", request.user.username),
	}
	return render(request, 'about/doctorabout.html', context)

def pharmacistAbout(request):
	context = {
		'username': re.sub(r"(\w)([A-Z])", r"\1 \2", request.user.username),
	}
	return render(request, 'about/pharmacistabout.html', context)

def help(request):
	allPatients = models.PatientGroup.objects.all()
	for patient in allPatients:
		if patient.patientUsername == request.user.username: # check to see if logged in user is a patient
			return patientHelp(request) # if they are then call patientHelp
	allPharmacists = models.PharmacistGroup.objects.all()
	for pharmacist in allPharmacists:
		if pharmacist.pharmacistUsername == request.user.username: # check to see if logged in user is a pharmacist account
			return pharmacistHelp(request) # if they are then call pharmacistHelp
	allDoctors = models.DoctorGroup.objects.all()
	for doctor in allDoctors:
		if doctor.doctorUsername == request.user.username: # check to see if logged in user is a doctor
			return doctorHelp(request) # if they are then call doctorHelp
	return HttpResponse("Error: Your account isn't associated with any user group") # this line is only run if the logged in user isn't assigned to any group

def patientHelp(request):
	context = {
		'username': re.sub(r"(\w)([A-Z])", r"\1 \2", request.user.username),
	}
	return render(request, 'help/patienthelp.html', context)

def doctorHelp(request):
	context = {
		'username': 'Dr. ' + re.sub(r"(\w)([A-Z])", r"\1 \2", request.user.username),
	}
	return render(request, 'help/doctorhelp.html', context)

def pharmacistHelp(request):
	context = {
		'username': re.sub(r"(\w)([A-Z])", r"\1 \2", request.user.username),
	}
	return render(request, 'help/pharmacisthelp.html', context)

def account(request):
	allPatients = models.PatientGroup.objects.all()
	for patient in allPatients:
		if patient.patientUsername == request.user.username: # check to see if logged in user is a patient
			return patientAccount(request) # if they are then call patientHelp
	allPharmacists = models.PharmacistGroup.objects.all()
	for pharmacist in allPharmacists:
		if pharmacist.pharmacistUsername == request.user.username: # check to see if logged in user is a pharmacist account
			return pharmacistAccount(request) # if they are then call pharmacistHelp
	allDoctors = models.DoctorGroup.objects.all()
	for doctor in allDoctors:
		if doctor.doctorUsername == request.user.username: # check to see if logged in user is a doctor
			return doctorAccount(request) # if they are then call doctorHelp
	return HttpResponse("Error: Your account isn't associated with any user group") # this line is only run if the logged in user isn't assigned to any group

def patientAccount(request):
	allDoctorPatient = models.DoctorPatient.objects.all()
	yourDoctors = []
	yourDoctorsPendingApproval = []
	for doctorPatientRelationship in allDoctorPatient:
		if doctorPatientRelationship.patientUsername == request.user.username:
			if doctorPatientRelationship.relationshipConfirmed:
				yourDoctors.append(doctorPatientRelationship.doctorUsername)
			else:
				yourDoctorsPendingApproval.append(doctorPatientRelationship.doctorUsername)
	allCollectors = models.PrescriptionCollector.objects.all()
	yourCollectors = []
	for collector in allCollectors:
		if collector.patientUsername == request.user.username:
			yourCollectors.append(collector.collectorName)
	context = {
		'username': re.sub(r"(\w)([A-Z])", r"\1 \2", request.user.username),
		'doctors': yourDoctors,
		'collectors': yourCollectors,
		'pendingDoctors': yourDoctorsPendingApproval,
	}
	return render(request, 'account/patientaccount.html', context)

def doctorAccount(request):
	context = {
		'username': 'Dr. ' + re.sub(r"(\w)([A-Z])", r"\1 \2", request.user.username),
	}
	return render(request, 'account/doctoraccount.html', context)

def pharmacistAccount(request):
	context = {
		'username': re.sub(r"(\w)([A-Z])", r"\1 \2", request.user.username),
	}
	return render(request, 'account/pharmacistaccount.html', context)

def prescribe(request):
	allDoctorPatientAssignmentsDoctorPatient = models.DoctorPatient.objects.all()
	patients = [] # pateints assigned to this doctor
	for doctorPatientRelationship in allDoctorPatientAssignmentsDoctorPatient:
		if doctorPatientRelationship.doctorUsername == request.user.username:
			if doctorPatientRelationship.relationshipConfirmed == True:
				patients.append(doctorPatientRelationship.patientUsername)
	pharmacies = []
	allPharmacies = models.PharmacistGroup.objects.all()
	for pharmacy in allPharmacies:
		pharmacies.append(pharmacy.pharmacistUsername)
	context = {
		'username': 'Dr. ' + re.sub(r"(\w)([A-Z])", r"\1 \2", request.user.username),
		'patients': patients,
		'pharmacies': pharmacies,
	}
	return render(request, 'prescribe-medication/prescribe.html', context)

def managepatients(request):
	allDoctorPatientAssignmentsDoctorPatient = models.DoctorPatient.objects.all()
	patients = [] # pateints assigned to this doctor
	for doctorPatientRelationship in allDoctorPatientAssignmentsDoctorPatient:
		if doctorPatientRelationship.doctorUsername == request.user.username:
			patients.append(doctorPatientRelationship.patientUsername)
	context = {
		'username': 'Dr. ' + re.sub(r"(\w)([A-Z])", r"\1 \2", request.user.username),
		'patients': patients,
	}
	return render(request, 'manage-patients/manage-patients.html', context)

def addPatient(request):
	doctor = request.user.username
	patient = request.POST.get('patient-username')
	if (doctor is not None) and (patient is not None) and (doctor != '') and (patient != ''):
		doctorPatientRelationship = models.DoctorPatient(doctorUsername = doctor, patientUsername = patient, relationshipConfirmed = False)
		doctorPatientRelationship.save()
	context = {
		'username': 'Dr.' + re.sub(r"(\w)([A-Z])", r"\1 \2", request.user.username),
	}
	return managepatients(request)

def removePatient(request):
	doctor = request.user.username
	patient = request.POST.get('remove-patient')
	if (doctor is not None) and (patient is not None) and (doctor != '') and (patient != ''):
		allDoctorPatientAssignmentsDoctorPatient = models.DoctorPatient.objects.all()
		for doctorPatientRelationship in allDoctorPatientAssignmentsDoctorPatient:
			if (doctorPatientRelationship.doctorUsername == doctor) and (doctorPatientRelationship.patientUsername == patient):
				doctorPatientRelationship.delete()
	context = {
		'username': 'Dr. ' + re.sub(r"(\w)([A-Z])", r"\1 \2", request.user.username),
	}
	return managepatients(request)

def addCollector(request):
	patient = request.user.username
	newCollector = request.POST.get('collector-name')
	newCollectorModel = models.PrescriptionCollector(patientUsername = patient, collectorName = newCollector)
	newCollectorModel.save()
	return patientAccount(request)

def removeCollector(request):
	patient = request.user.username
	allPatientCollectors = models.PrescriptionCollector.objects.all()
	for patientCollector in allPatientCollectors:
		if patientCollector.patientUsername == patient and (patientCollector.collectorName in request.POST):
			print ("test")
			patientCollector.delete()
	return patientAccount(request)

def approveDoctor(request):
	allDoctorPatientAssignments = models.DoctorPatient.objects.all()
	for doctorPatientRelationship in allDoctorPatientAssignments:
		if (doctorPatientRelationship.doctorUsername in request.POST):
			if doctorPatientRelationship.patientUsername == request.user.username:
				doctorPatientRelationship.relationshipConfirmed = True
				doctorPatientRelationship.save()
	context = {
		'username': re.sub(r"(\w)([A-Z])", r"\1 \2", request.user.username),
	}
	return patientAccount(request)

def removeDoctor(request):
	allDoctorPatientAssignments = models.DoctorPatient.objects.all()
	for doctorPatientRelationship in allDoctorPatientAssignments:
		if (doctorPatientRelationship.doctorUsername in request.POST):
			if doctorPatientRelationship.patientUsername == request.user.username:
				doctorPatientRelationship.relationshipConfirmed = False
				doctorPatientRelationship.save()
	context = {
		'username': re.sub(r"(\w)([A-Z])", r"\1 \2", request.user.username),
	}
	return patientAccount(request)

def writePrescription(request):
	doctor = request.user.username
	patient = request.POST.get('patient')
	pharmacy = request.POST.get('pharmacy')
	prescription = models.Prescription(comment = request.POST.get('comment0'), dateIssued = date.today(), dispensed = False, doctorId = doctor, patientId = patient,
		pharmacyId = pharmacy)
	prescription.save()
	i = 0
	while True:
		drug = request.POST.get('drug' + str(i))
		if drug is None: # if we've reached the end of the drugs list
			break # then break
		for key, value in request.POST.items():
			print('Key: %s' % (key) ) 
			print('Value %s' % (value) )
		dosageForm = request.POST.get('dosage-form' + str(i))
		doseValue = request.POST.get('dose-value' + str(i))
		doseUnit = request.POST.get('dose-unit' + str(i))
		durationValue = request.POST.get('duration-value' + str(i))
		durationUnit = request.POST.get('duration-unit' + str(i))
		frequency = request.POST.get('frequency' + str(i))
		route = request.POST.get('route' + str(i))
		quantity = request.POST.get('quantity' + str(i))
		status = request.POST.get('status' + str(i))
		videoRequired = False
		if request.POST.get('video-required' + str(i)) == 'on':
			videoRequired = True
		comment = request.POST.get('comment' + str(i))
		item = models.Item(dosageForm = dosageForm, doseValue = doseValue, doseUnit = doseUnit, drug = drug, durationValue = durationValue, 
			durationUnit = durationUnit, frequency = frequency, route = route, quantity = quantity, status = status, 
			videoRequired = videoRequired, videoURL =  generateTenDigtURL())
		item.save()
		prescriptionItem = models.PrescriptionItem(prescription=prescription, item = item)
		prescriptionItem.save()
		i += 1
	return home(request)

def markDispensed(request, prescriptionId):
	allPrescriptions = models.Prescription.objects.all()
	for prescription in allPrescriptions:
		if str(prescription.id) == str(prescriptionId):
			prescription.dateDispensed = date.today()
			prescription.dispensed = True
			prescription.save()
	return redirect('/home')

def markReceived(request, prescriptionId):
	allPrescriptions = models.Prescription.objects.all()
	for prescription in allPrescriptions:
		if str(prescription.id) == str(prescriptionId):
			prescription.dateReceived = date.today()
			prescription.save()
	return redirect('/home')

def generatePrescriptionQRs(request, prescriptionId):
	items = []
	allPrescriptions = models.Prescription.objects.all()
	for prescription in allPrescriptions:
		if str(prescription.id) == str(prescriptionId):
			items = getPrescriptionItems(prescription)
			break
	imageUrls = []
	for item in items:
		qrcodes.createQR(item.videoURL)
		imageUrls.append('http://127.0.0.1:8000/' + 'media/QR-Codes/' + item.videoURL + '.svg')
	
	context = {
		'username': re.sub(r"(\w)([A-Z])", r"\1 \2", request.user.username),
		'itemURLs': zip(items, imageUrls),
	}
	return render(request, 'print-qrcodes/print-qrcodes.html', context)

def drugInteractions(request):
	context = {
		'username': re.sub(r"(\w)([A-Z])", r"\1 \2", request.user.username),
	}
	return render(request, 'comprehensive_conflicts/comprehensive_conflicts.html', context)

def checkInteractions(request):
	pharmacist = request.user.username
	drug1 = request.POST.get('search1')
	drug2 = request.POST.get('search2')
	interactions = []
	if drug2 == '':
		interactions = rxnavAPI.getInteractionsSingleDrug(drug1)
	else:
		interactions = rxnavAPI.getInteractionsBetweenDrugs(drug1, drug2)
	context = {
		'username': re.sub(r"(\w)([A-Z])", r"\1 \2", request.user.username),
		'interactions': interactions,
		'drug1' : drug1,
		'drug2': drug2,
	}
	return render(request, 'comprehensive_conflicts/comprehensive_conflicts.html', context)

def getCollectors(patient):
	allCollectors = models.PrescriptionCollector.objects.all()
	collectorsForPatient = []
	for collector in allCollectors:
		if collector.patientUsername == patient:
			collectorsForPatient.append(collector.collectorName)
	return collectorsForPatient
