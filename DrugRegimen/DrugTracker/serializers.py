from rest_framework import serializers
from .models import DrugConflict

class DrugConflictSerializer (serializers.HyperlinkedModelSerializer):
	class Meta:
		model = DrugConflict
		fields = ('drug1', 'drug2', 'conflictSeverity', 'conflictNotes')
