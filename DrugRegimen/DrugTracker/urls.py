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
    path('help', views.help, name='help'),
    path('dose/<doseURL>/', views.takeDose, name='takeDose'),
    path('upload', views.upload, name='upload'),
	path('api', include(router.urls)),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]