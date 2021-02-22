# Generated by Django 3.0.4 on 2021-02-21 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DrugTracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DrugConflict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drug1', models.CharField(max_length=50)),
                ('drug2', models.CharField(max_length=50)),
                ('conflictSeverity', models.CharField(max_length=50)),
                ('conflictNotes', models.CharField(max_length=50)),
            ],
        ),
    ]