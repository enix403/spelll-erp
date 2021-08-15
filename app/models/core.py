from __future__ import annotations
from django.db import models
from . import fields

from typing import ClassVar, TypeVar, Generic

T = TypeVar('T', bound='BaseModel')

class BaseModel(Generic[T], models.Model):
    objects: ClassVar[models.Manager[T]]

    class Meta:
        abstract = True


class Station(BaseModel['Station']):
    class Meta:
        db_table = "spl1_stations"

    name = models.CharField(max_length=20, db_column="name")
    colleges: models.Manager[College]

class College(BaseModel['College']):
    class Meta:
        db_table = "spl1_colleges"
        
    name = models.CharField(max_length=20, db_column="name")
    station = fields.make_fk(Station, "station_id", 'colleges')

    admissions: models.Manager[Admission]

class Discipline(BaseModel['Discipline']):
    class Meta:
        db_table = 'spl1_disciplines'

    name = models.CharField(max_length=255)
    level = models.SmallIntegerField()

    fee_structures: models.Manager[FeeStructure]

class FeeStructure(BaseModel['FeeStructure']):
    class Meta:
        db_table = 'spl1_fee_structures'

    discipline = fields.make_fk(Discipline, 'discipline_id', 'fee_structures')
    full_fee = models.PositiveIntegerField()
    slabs: models.Manager[FeeSlab]

class FeeSlab(BaseModel['FeeSlab']):
    class Meta:
        db_table = 'spl1_fee_slabs'

    name = models.CharField(max_length=255)
    index = fields.PositiveTinyIntegerField()
    marks = models.PositiveSmallIntegerField()
    amount = models.PositiveIntegerField()

    parent_fee_structure = fields.make_fk(FeeStructure, 'fee_structure_id', 'slabs')


class DiscountPreset(BaseModel['DiscountPreset']):
    class Meta:
        db_table = 'spl1_discount_presets'
    name = models.CharField(max_length=255)
    amount = models.SmallIntegerField()


class Admission(BaseModel['Admission']):
    class Meta:
        db_table = 'spl1_admissions'

    college = fields.make_fk(College, 'college_id', 'admissions')
    name = models.CharField(max_length=255)
    gender = fields.PositiveTinyIntegerField()
    cnic = models.CharField(max_length=255)

    father_name = models.CharField(max_length=255)
    father_cnic = models.CharField(max_length=255)
    # school = models.CharField(max_length=255)
    # address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    date_of_birth = models.DateField()

    level = fields.PositiveTinyIntegerField()
    discipline = fields.make_fk(Discipline, 'discipline_id')
    session = fields.PositiveTinyIntegerField()
    adm_type = fields.PositiveTinyIntegerField()
    semOrYear = fields.PositiveTinyIntegerField()

    marks = models.PositiveSmallIntegerField()

    full_fee = models.PositiveIntegerField()
    marks_based_disc = models.PositiveIntegerField()
    # other_discount = fields.make_fk(DiscountPreset, 'other_discount_id')
    discretion_disc = models.PositiveIntegerField()
    discretion_disc_reason = models.CharField(max_length=255)
    # total_disc = models.PositiveIntegerField()

    pfy_amount = models.PositiveIntegerField()
    final_package = models.PositiveIntegerField()
    num_installments = fields.PositiveTinyIntegerField()
    adm_amount = models.PositiveIntegerField()

