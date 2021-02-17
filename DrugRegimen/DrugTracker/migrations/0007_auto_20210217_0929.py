# Generated by Django 3.0.4 on 2021-02-17 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DrugTracker', '0006_doctorgroup_patientgroup_pharmacistgroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='medconflict',
            name='conflictDetails',
            field=models.CharField(default='', max_length=700),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medication',
            name='medicationNotes',
            field=models.CharField(default='', max_length=700),
            preserve_default=False,
        ),
    ]
