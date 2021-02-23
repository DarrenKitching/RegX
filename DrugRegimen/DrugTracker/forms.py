from django.db import models
from django import forms

class VideoSubmission(forms.Form):
	uploadDate = forms.DateField()
	# doseCount = forms.IntegerField() # e.g. if you need to take two tablets of the same drug a day you'd have one video for doseCount 1 and another for doseCount 2
	video = forms.FileField()