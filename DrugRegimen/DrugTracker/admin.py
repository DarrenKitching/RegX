from django.contrib import admin
from .models import Prescription, PatientGroup, PharmacistGroup, DoctorGroup

admin.site.register(Prescription)
admin.site.register(PatientGroup)
admin.site.register(PharmacistGroup)
admin.site.register(DoctorGroup)
# Register your models here.
