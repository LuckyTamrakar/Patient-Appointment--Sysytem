# Generated by Django 3.2.12 on 2022-04-07 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0012_alter_appointment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
