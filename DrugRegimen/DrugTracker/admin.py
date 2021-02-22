from django.contrib import admin
from .models import *

admin.site.register(DrugConflict)
admin.site.register(DrugNotes)
admin.site.register(Prescription)
admin.site.register(PatientGroup)
admin.site.register(PharmacistGroup)
admin.site.register(DoctorGroup)
# Register your models here.
