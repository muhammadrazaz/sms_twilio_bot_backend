# Generated by Django 5.1.2 on 2024-10-29 11:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0003_alter_agentprofile_channel_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentprofile',
            name='uan',
            field=models.CharField(blank=True, max_length=12, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+1XXXXXXXXXX' or 'XXXXXXXXXX'.", regex='^\\+?1?\\d{10}$')]),
        ),
    ]
