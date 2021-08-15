from __future__ import annotations
from __future__ import annotations
from django.shortcuts import redirect
from django.urls import reverse
# from typing import Any, ClassVar, Generic, TypeVar, Type
# from django.db.models import Model, Manager
# from django.db import models


# from functools import cached_property

# T = TypeVar('T', bound='Base')

# class Base(Generic[T], Model):
#     @property
#     @classmethod
#     def objects(cls: Type[T]) -> Manager[T]: ... 


# class Child(Base['Child']):
#     name = 45
#     kop: Child

def index(request):
    return redirect(reverse('manage'))
