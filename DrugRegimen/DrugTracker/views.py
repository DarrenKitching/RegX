from django.shortcuts import render
from django.http import HttpResponse
import datetime
from datetime import date
from . import models

# login page
def index(request):
    return render(request, 'login.html')

# patient home screen
def home(request):
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
					myPerscriptions.append(getMedicationName(perscription.medicationCode) + ", Dose: " + perscription.medicationDose)
	context = {
		'now': now,
		'medications': myPerscriptions,
		}
	return render(request, 'home.html', context)

# use medication code number to get the medication's name
def getMedicationName(medicationCode):
	allMedications = models.Medication.objects.all()
	for medication in allMedications:
		if medicationCode == medication.medicationCode:
			return medication.medicationName
	return "" # no medication with that code has been found