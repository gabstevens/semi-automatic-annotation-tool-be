# Generated by Django 2.2.5 on 2020-11-16 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_api', '0011_detector_is_both'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='thermal_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
