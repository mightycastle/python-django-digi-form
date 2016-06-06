# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-28 06:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_document', '0002_auto_20160528_0133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formdocumentsource',
            name='company_share',
        ),
        migrations.RemoveField(
            model_name='formdocumentsource',
            name='user_share',
        ),
        migrations.RemoveField(
            model_name='formdocumentresponse',
            name='form_source',
        ),
        migrations.AddField(
            model_name='formdocumentresponse',
            name='first_name',
            field=models.CharField(default='First', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='formdocumentresponse',
            name='last_name',
            field=models.CharField(default='Last', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='formdocumentresponse',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='formdocumentresponse',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.DeleteModel(
            name='FormDocumentSource',
        ),
    ]