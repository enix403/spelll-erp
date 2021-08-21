from django.db import models

from . import fields
from .core import BaseModel, College

class Section(BaseModel['Section']):
    class Meta:
        db_table = 'spl1_sections'

    name = models.CharField(max_length=25)
    college = fields.make_fk(College, 'college_id', 'sections')

