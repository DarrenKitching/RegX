from django.contrib import admin
from .models import *

admin.site.register(DrugConflict)
admin.site.register(DrugNotes)
admin.site.register(Prescription)
admin.site.register(PatientGroup)
admin.site.register(PharmacistGroup)
admin.site.register(DoctorGroup)
admin.site.register(Item)
admin.site.register(PrescriptionItem)
# Register your models here.
