# Generated by Django 2.0.1 on 2018-01-24 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_auto_20180124_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='file',
            field=models.FilePathField(null=True),
        ),
    ]
