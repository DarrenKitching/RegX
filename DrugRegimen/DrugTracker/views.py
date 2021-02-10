from django.shortcuts import render
from django.http import HttpResponse
import datetime
from datetime import date
from . import models
from . import qrcodes

def index(request):
	"""
	This function is run when the user opens the site at http://127.0.0.1:8000

    This function will display login.html in the user's web browser.

    Args:
        request (request): Request is built in to django and stores the current state of the system e.g. the username of the logged in user.

    Returns:
        render: Will render the login.html file.
	"""
	return render(request, 'login.html')

def home(request):
	"""
	This function is run when the user has logged in and gets brought to http://127.0.0.1:8000/home

    This function will display home.html in the user's web browser. It will pass in a list of perscriptions which the user needs to 
    take today into home.html

    Args:
        request (request): Request is built in to django and stores the current state of the system e.g. the username of the logged in user.

    Returns:
        render: Will render the home.html file with the list of the user's perscriptions that need to be taken today.

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
	return render(request, 'home.html', context)

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