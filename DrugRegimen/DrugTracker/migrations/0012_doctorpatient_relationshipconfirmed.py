# Generated by Django 3.0.4 on 2021-03-15 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DrugTracker', '0011_auto_20210308_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorpatient',
            name='relationshipConfirmed',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]