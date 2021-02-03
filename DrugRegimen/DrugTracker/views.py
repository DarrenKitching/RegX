from django.shortcuts import render
from django.http import HttpResponse
import datetime
from . import models
# Create your views here.

def index(request):
    return render(request, 'login.html')

def home(request):
    now = datetime.datetime.now()
    allPerscriptions = models.Perscription.objects.all()
    allMedications = models.Medication.objects.all()
    myPerscriptions = []
    for perscription in allPerscriptions:
    	if perscription.patient == request.user.username:
    		myPerscriptions.append(getMedicationName(perscription.medicationCode) + ", Dose: " + perscription.medicationDose)
    context = {
    	'now': now,
    	'medications': myPerscriptions,
    }
    return render(request, 'home.html', context)

def getMedicationName(medicationCode):
	allMedications = models.Medication.objects.all()
	for medication in allMedications:
		if medicationCode == medication.medicationCode:
			return medication.medicationName
	return ""