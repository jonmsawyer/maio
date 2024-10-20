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

from maio.validators import validate_rating

class RatingMeta(ModelBase):
    '''Metaclass for Rating model.'''
    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        app_label = 'maio'
        db_table_comment = 'Contains the Ratings for Media.'
        get_latest_by = ['-date_modified']
        # order_with_respect_to = ['user', 'date_added']
        ordering = ['-date_modified']
        # indexes = [
        #     Index(fields=('sort', 'name', 'is_default', 'date_added', '-date_modified'))
        # ]


class Rating(Model, metaclass=RatingMeta):
    '''Rating model.'''
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = ForeignKey(to='MaioUser', on_delete=CASCADE)
    media = ForeignKey(to='Media', on_delete=CASCADE)
    rating = PositiveSmallIntegerField('Rating', default=0, validators=[validate_rating])
    date_added = DateTimeField(auto_now_add=True)
    date_modified = DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} Ratings {self.media}"
