from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import ArrayField
from core.models import (
    TimeStampedModel,
    StatusModel,
)


class DataSourceModel(TimeStampedModel, StatusModel, models.Model):
    source_name = models.CharField(max_length=64)
    columns = ArrayField(
        models.CharField(max_length=32, blank=True)
    )
    model_name = models.CharField(max_length=64)



class AFSLicenseeEntry(TimeStampedModel, models.Model):
    name = models.CharField(max_length=256)
    license_no = models.IntegerField()
    abn = models.IntegerField()
    commenced_date = models.DateField(null=True)
    service_address = models.CharField(max_length=512)
    status = models.CharField(max_length=32)
    principle_business_address = models.CharField(max_length=512)


class AFSAuthorisedRepresentative(TimeStampedModel, models.Model):
    name = models.CharField(max_length=256)
    license_no = models.IntegerField()
    licensed_by = models.ForeignKey(AFSLicenseeEntry, null=True)

