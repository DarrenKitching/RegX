# Generated by Django 3.0.4 on 2021-04-05 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DrugTracker', '0012_doctorpatient_relationshipconfirmed'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrescriptionCollector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patientUsername', models.CharField(max_length=50)),
                ('collectorName', models.CharField(max_length=50)),
            ],
        ),
    ]
