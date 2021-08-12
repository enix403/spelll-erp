from django.db import models
from . import fields

class BaseModel(models.Model):
    objects: models.Manager
    class Meta:
        abstract = True


class Station(BaseModel):
    class Meta:
        db_table = "sl_stations"

    name = models.CharField(max_length=20, db_column="name")
    colleges: models.Manager

class College(BaseModel):
    class Meta:
        db_table = "sl_colleges"
        
    name = models.CharField(max_length=20, db_column="name")
    station = fields.make_foreign_key(Station, "station_id", 'colleges')

    admissions: models.Manager

class Discipline(BaseModel):
    class Meta:
        db_table = 'sl_disciplines'

    name = models.CharField(max_length=255)
    level = models.SmallIntegerField()

    fee_structures: models.Manager

class FeeStructure(BaseModel):
    class Meta:
        db_table = 'sl_fee_structures'

    discipline = fields.make_foreign_key(Discipline, 'discipline_id', 'fee_structures')
    full_fee = models.PositiveIntegerField()
    slabs: models.Manager

class FeeSlab(BaseModel):
    class Meta:
        db_table = 'sl_fee_slabs'

    name = models.CharField(max_length=255)
    index = fields.PositiveTinyIntegerField()
    marks = models.PositiveSmallIntegerField()
    amount = models.PositiveIntegerField()

    parent_fee_structure = fields.make_foreign_key(FeeStructure, 'fee_structure_id', 'slabs')


class DiscountPreset(BaseModel):
    name = models.CharField(max_length=255)
    amount = models.SmallIntegerField()


class Admission(BaseModel):
    class Meta:
        db_table = 'sl_admissions'

    college = fields.make_foreign_key(College, 'college_id', 'admissions')
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
    discipline = fields.make_foreign_key(Discipline, 'discipline_id')
    session = fields.PositiveTinyIntegerField()
    adm_type = fields.PositiveTinyIntegerField()
    semOrYear = fields.PositiveTinyIntegerField()

    marks = models.PositiveSmallIntegerField()

    full_fee = models.PositiveIntegerField()
    marks_based_disc = models.PositiveIntegerField()
    # other_discount = fields.make_foreign_key(DiscountPreset, 'other_discount_id')
    discretion_disc = models.PositiveIntegerField()
    discretion_disc_reason = models.CharField(max_length=255)
    # total_disc = models.PositiveIntegerField()

    pfy_amount = models.PositiveIntegerField()
    final_package = models.PositiveIntegerField()
    num_installments = fields.PositiveTinyIntegerField()
    adm_amount = models.PositiveIntegerField()

