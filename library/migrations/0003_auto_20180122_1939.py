# Generated by Django 2.0.1 on 2018-01-22 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_auto_20180118_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='image',
            field=models.FileField(blank=True, default='no-image.gif', null=True, upload_to=''),
        ),
    ]
