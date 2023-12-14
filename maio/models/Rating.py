'''
File: Rating.py

Module: ``maio.models.Rating``
'''

from __future__ import annotations

import uuid

from django.db.models import (
    Model, UUIDField, DateTimeField, ForeignKey, PositiveSmallIntegerField, CASCADE,
)
from django.db.models.base import ModelBase

from .MaioUser import MaioUser
from .Media import Media


class RatingMeta(ModelBase):
    '''Metaclass for Rating model.'''
    ordering = ['-date_added']


class Rating(Model, metaclass=RatingMeta):
    '''Rating model.'''
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = ForeignKey(to=MaioUser, on_delete=CASCADE)
    media = ForeignKey(to=Media, on_delete=CASCADE)
    rating = PositiveSmallIntegerField('Rating', default=0)
    date_added = DateTimeField(auto_now_add=True)
    date_modified = DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} Ratings {self.media}"
