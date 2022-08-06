# Generated by Django 4.0.6 on 2022-08-04 21:05

from django.db import migrations, models
import event.utils


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='cover',
            field=models.ImageField(null=True, upload_to=event.utils.PathAndHash('events/covers')),
        ),
        migrations.AlterField(
            model_name='event',
            name='number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterModelTable(
            name='event',
            table='events',
        ),
    ]
