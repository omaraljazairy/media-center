# Generated by Django 2.0.3 on 2018-04-01 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alarmclock', '0036_auto_20180401_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarms',
            name='executed',
            field=models.DateTimeField(),
        ),
    ]
