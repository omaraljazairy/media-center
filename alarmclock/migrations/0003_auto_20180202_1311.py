# Generated by Django 2.0.1 on 2018-02-02 13:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('alarmclock', '0002_auto_20180202_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarms',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alarms',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
