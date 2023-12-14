'''
File: Like.py

Module: ``maio.models.Like``
'''

from __future__ import annotations

import uuid

from django.db.models import Model, UUIDField, DateTimeField, ForeignKey, CASCADE
from django.db.models.base import ModelBase

from .MaioUser import MaioUser
from .Media import Media


class LikeMeta(ModelBase):
    '''Metaclass for Like model.'''
    ordering = ['-date_added']


class Like(Model, metaclass=LikeMeta):
    '''Like model.'''
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = ForeignKey(to=MaioUser, on_delete=CASCADE)
    media = ForeignKey(to=Media, on_delete=CASCADE)
    date_added = DateTimeField(auto_now_add=True)
    date_modified = DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} Likes {self.media}"
