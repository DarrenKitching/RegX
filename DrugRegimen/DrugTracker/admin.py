from django.contrib import admin
from .models import Perscription, Medication, MedConflict, DoseURL, PatientGroup, PharmacistGroup, DoctorGroup

admin.site.register(Perscription)
admin.site.register(Medication)
admin.site.register(MedConflict)
admin.site.register(DoseURL)
admin.site.register(PatientGroup)
admin.site.register(PharmacistGroup)
admin.site.register(DoctorGroup)
# Register your models here.
