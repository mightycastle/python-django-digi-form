# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-21 11:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_auto_20160821_0959'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='price_cents_monthly',
            new_name='price_cents',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='price_cents_yearly',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='trial_months_available',
        ),
        migrations.AddField(
            model_name='plan',
            name='recurring_type',
            field=models.CharField(choices=[('D', 'Day'), ('W', 'Week'), ('M', 'Month'), ('Y', 'Year')], default='M', max_length=1),
        ),
        migrations.AddField(
            model_name='plan',
            name='trial_days',
            field=models.SmallIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='plansubscription',
            name='recurring_type',
            field=models.CharField(choices=[('D', 'Day'), ('W', 'Week'), ('M', 'Month'), ('Y', 'Year')], max_length=1),
        ),
    ]