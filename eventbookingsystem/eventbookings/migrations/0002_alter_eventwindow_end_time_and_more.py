# Generated by Django 4.0.2 on 2022-02-22 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbookings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventwindow',
            name='end_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='eventwindow',
            name='start_time',
            field=models.TimeField(),
        ),
    ]
