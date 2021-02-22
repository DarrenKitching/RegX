from rest_framework import serializers
from .models import DrugConflict, DrugNotes

class DrugConflictSerializer (serializers.HyperlinkedModelSerializer):
	class Meta:
		model = DrugConflict
		fields = ('drug1', 'drug2', 'conflictSeverity', 'conflictNotes')

class DrugNotesSerializer (serializers.HyperlinkedModelSerializer):
	class Meta:
		model = DrugNotes
		fields = ('drug', 'notes')