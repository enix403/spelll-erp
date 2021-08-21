from __future__ import annotations
from django.db import models
from . import fields

from typing import TYPE_CHECKING, ClassVar, TypeVar, Generic
if TYPE_CHECKING:
    from .sectioning import Section

T = TypeVar('T', bound='BaseModel')

class BaseModel(models.Model, Generic[T]):
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
    sections: models.Manager[Section]

class Discipline(BaseModel['Discipline']):
    class Meta:
        db_table = 'spl1_disciplines'

    name = models.CharField(max_length=30)