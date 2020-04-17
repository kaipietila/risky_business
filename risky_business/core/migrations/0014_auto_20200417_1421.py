# Generated by Django 3.0.4 on 2020-04-17 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_phrase'),
    ]

    operations = [
        migrations.AddField(
            model_name='acceptableusepolicyrule',
            name='decision',
            field=models.CharField(choices=[('Allow', 'ALLOW'), ('Reject', 'REJECT'), ('Alert', 'ALERT')], max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='acceptableusepolicyrule',
            name='hit_message',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
