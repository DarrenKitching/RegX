from django.contrib.auth.models import User
import django
from . import models

def createNewUser(username, password):
	newUser = User(username=username)
	newUser.set_password(password)
	newUser.is_superuser = True
	newUser.is_staff = True
	newUser.save()
	newPatient = models.PatientGroup(patientUsername=username)
	newPatient.save()