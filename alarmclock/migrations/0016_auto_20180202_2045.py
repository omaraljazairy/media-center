# Generated by Django 2.0.1 on 2018-02-02 20:45

import alarmclock.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alarmclock', '0015_auto_20180202_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarms',
            name='playlist',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='alarm_playlist', to='library.Playlist', validators=[alarmclock.validators.validate_playlist]),
        ),
    ]
