# Generated by Django 3.0.4 on 2021-02-10 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DrugTracker', '0005_medconflict'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctorUsername', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PatientGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patientUsername', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PharmacistGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pharmacistUsername', models.CharField(max_length=50)),
            ],
        ),
    ]