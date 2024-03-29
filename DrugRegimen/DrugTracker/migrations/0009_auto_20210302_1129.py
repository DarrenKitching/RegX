# Generated by Django 3.0.4 on 2021-03-02 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DrugTracker', '0008_auto_20210302_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='dateDispensed',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='dateReceived',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='pharmacyNote',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
