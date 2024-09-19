'''
File: KeyValue.py

Module: ``maio.models.KeyValue``
'''

from __future__ import annotations

import uuid
from uuid import UUID
from hashlib import sha3_512

from django.conf import settings
from django.db.models import (
    Model, UUIDField, ForeignKey, CASCADE,
)
from django.db.models.base import ModelBase
from django.contrib.auth.models import User


class MaioUserMeta(ModelBase):
    '''Metaclass for MaioUser model.'''
    class Meta:
        verbose_name = 'Maio User'
        verbose_name_plural = 'Maio Users'
        app_label = 'maio'
        db_table_comment = 'Maio users are also Django users.'
        # get_latest_by = ['-user__last_login']
        # order_with_respect_to = ['user']
        # ordering = ['user.last_login']
        # indexes = [
        #     Index(fields=('sort', 'name', 'is_default', 'date_added', '-date_modified'))
        # ]


class MaioUser(Model, metaclass=MaioUserMeta):
    '''MaioUser model.'''
    id = UUIDField('UUID', primary_key=True, default=uuid.uuid4, editable=False)
    user = ForeignKey(User, on_delete=CASCADE, editable=False)

    def __str__(self) -> str:
        return str(self.user)

    @staticmethod
    def default() -> UUID:
        '''Return the default user for this application.'''
        try:
            return User.objects.get(username='Maio').id
        except User.DoesNotExist:
            data = {
                'username': 'Maio',
                'email': 'maio@example.com',
                'password': (
                    sha3_512(bytes(settings.SECRET_KEY, encoding='UTF-8')).hexdigest()
                ),
            }
            user = User.objects.create_user(**data)
            return user.id
