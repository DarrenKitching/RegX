from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'drugconflicts', views.DrugConflictViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('dose/<doseURL>/', views.takeDose, name='takeDose'),
	path('api', include(router.urls)),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]