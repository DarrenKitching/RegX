# Generated by Django 3.0.4 on 2021-03-04 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DrugTracker', '0009_auto_20210302_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='startDate',
            field=models.DateField(null=True),
        ),
    ]