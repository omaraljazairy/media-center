# Generated by Django 2.0.3 on 2018-04-02 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alarmclock', '0038_auto_20180402_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarms',
            name='test',
            field=models.DateTimeField(db_index=True, default='2018-01-01 00:00:00'),
        ),
        migrations.AlterField(
            model_name='alarms',
            name='executed',
            field=models.DateTimeField(db_index=True),
        ),
    ]
