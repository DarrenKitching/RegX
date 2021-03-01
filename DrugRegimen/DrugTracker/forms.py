from django import forms

class UploadFileForm(forms.Form):
    doseURL = forms.CharField(max_length=50)
    video = forms.FileField()