# Generated by Django 4.0.6 on 2022-08-05 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_event_students'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='students',
            new_name='members',
        ),
    ]
