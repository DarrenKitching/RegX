from django.shortcuts import render
from django.http import HttpResponse
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
	print(generateTenDigtURL())
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

    This function will display patienthome.html in the user's web browser. It will pass in a list of perscriptions which the user needs to 
    take today into home.html

    Args:
        request (request): Request is built in to django and stores the current state of the system e.g. the username of the logged in user.

    Returns:
        render: Will render the patienthome.html file with the list of the user's perscriptions that need to be taken today.

    """
	url = 'http://uca.edu' # testing QRcode generation - delete later
	qrcodes.createQR(url) # testing QRcode generation - delete later
	now = datetime.datetime.now()
	today = date.today()
	allPerscriptions = models.Perscription.objects.all()
	allMedications = models.Medication.objects.all()
	myPerscriptions = []
	for perscription in allPerscriptions:
		if perscription.patient == request.user.username:
			dayDifference = (today - perscription.perscriptionStartDate).days
			if dayDifference % perscription.intervalBetweenDoses == 0: # check that today is a day where you should be taking your perscription
				dosesTaken = ((dayDifference - 1) // perscription.intervalBetweenDoses) * perscription.timesPerDay # count number of doses you've already taken
				if perscription.totalNumberOfDoses > dosesTaken: # make sure you haven't already taken all of your doses for this medication
					myPerscriptions.append(getMedicationName(perscription.medicationCode) + ", Dose: " + str(perscription.medicationDose) +perscription.doseUnit)
	context = {
		'now': now,
		'medications': myPerscriptions,
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
	return render(request, 'doctorhome.html')

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
