# Generated by Django 3.2.12 on 2022-04-09 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0022_alter_appointment_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='created',
        ),
    ]
