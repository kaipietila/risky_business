# Generated by Django 3.0.4 on 2020-04-12 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200407_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acceptableusepolicyrule',
            name='full_rule',
            field=models.CharField(max_length=512),
        ),
    ]
