# Generated by Django 2.0.1 on 2018-02-26 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alarmclock', '0031_auto_20180222_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queuedsongs',
            name='played',
            field=models.DateTimeField(db_index=True, verbose_name='Song played time'),
        ),
    ]
