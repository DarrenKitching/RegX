from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'drugconflicts', views.DrugConflictViewSet)
router.register(r'drugnotes', views.DrugNotesViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('about', views.about, name='about'),
    path('account', views.account, name='account'),
    path('manage', views.managepatients, name='managepatients'),
    path('prescribe', views.prescribe, name='prescribe'),
    path('write-prescription', views.writePrescription, name='writePrescription'),
    path('help', views.help, name='help'),
    path('add-patient', views.addPatient, name='addPatient'),
    path('remove-patient', views.removePatient, name='removePatient'),
    path('dose/<doseURL>/', views.takeDose, name='takeDose'),
    path('mark-dispensed/<prescriptionId>/', views.markDispensed, name='markDispensed'),
    path('mark-received/<prescriptionId>/', views.markReceived, name='markReceived'),
    path('generateQRs/<prescriptionId>/', views.generatePrescriptionQRs, name='generateQRs'),
    path('upload', views.upload, name='upload'),
	path('api', include(router.urls)),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]