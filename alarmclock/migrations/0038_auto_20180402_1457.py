# Generated by Django 2.0.3 on 2018-04-02 14:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('alarmclock', '0037_auto_20180401_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarms',
            name='executed',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2018, 4, 2, 14, 57, 57, 877905, tzinfo=utc)),
        ),
    ]
