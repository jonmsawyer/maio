'''
File: Log.py

Module: ``maio.models.Log``
'''

from __future__ import annotations

import uuid

from django.http import HttpRequest
from django.db.models import (
    Model, UUIDField, ForeignKey, CharField, DateTimeField, TextField, TextChoices,
    DO_NOTHING,
)
from django.db.models.base import ModelBase
from django.utils.translation import gettext_lazy as _T

from .MaioUser import MaioUser


class LogLevelChoices(TextChoices):
    '''Log level choices.'''
    DEBUG = 'debug', _T('Debug')
    LOG = 'log', _T('Log')
    INFO = 'info', _T('Info')
    NOTICE = 'notice', _T('Notice')
    WARNING = 'warning', _T('Warning')
    ERROR = 'error', _T('Error')
    CRITICAL = 'critical', _T('Critical')
    ALERT = 'alert', _T('Alert')
    EMERGENCY = 'emergency', _T('Emergency')
    EXCEPTION = 'exception', _T('Exception')


class LogMeta(ModelBase):
    '''Metaclass for Log model.'''
    name = 'Log'
    verbose_name = 'Logs'
    app_label = 'maio'
    db_table_comment = 'Logs contain logging information, errors, warnings, etc.'
    get_latest_by = ['user', '-date_added']
    order_with_respect_to = ['user', 'date_added']
    # ordering = ['media', 'Log_date']


class Log(Model, metaclass=LogMeta):
    '''Log model.'''
    id = UUIDField('UUID', primary_key=True, default=uuid.uuid4, editable=False)
    user = ForeignKey(to=MaioUser, on_delete=DO_NOTHING)
    name = CharField('Name', max_length=254)
    level = CharField('Log Level', max_length=10, choices=LogLevelChoices.choices, default=LogLevelChoices.LOG)
    date_added = DateTimeField('Date Added', auto_now_add=True)
    message = TextField('Message')

    def __str__(self):
        return f"[{self.date_added}] - [{self.user} {self.level}] - {str(self.message)[0:20]}"

    @staticmethod
    def new(request: HttpRequest, name: str) -> Log:
        '''Create a new logger with the given name.'''
        user, _created = MaioUser.objects.get_or_create(user=request.user)
        return Log(user=user, name=name)

    def clear(self) -> None:
        self.id = None
        self.date_added = None
        self.message = None
        self.level = LogLevelChoices.LOG

    def debug(self, message: str) -> Log:
        '''Insert a DEBUG message.'''
        self.clear()
        self.level = LogLevelChoices.DEBUG
        self.message = message
        self.save()
        return self

    def log(self, message: str) -> Log:
        '''Insert a LOG message.'''
        self.clear()
        self.level = LogLevelChoices.LOG
        self.message = message
        self.save()
        return self

    def info(self, message: str) -> Log:
        '''Insert an INFO message.'''
        self.clear()
        self.level = LogLevelChoices.INFO
        self.message = message
        self.save()
        return self

    def notice(self, message: str) -> Log:
        '''Insert a NOTICE message.'''
        self.clear()
        self.level = LogLevelChoices.NOTICE
        self.message = message
        self.save()
        return self

    def warning(self, message: str) -> Log:
        '''Insert a WARNING message.'''
        self.clear()
        self.level = LogLevelChoices.WARNING
        self.message = message
        self.save()
        return self

    def error(self, message: str) -> Log:
        '''Insert a ERROR message.'''
        self.clear()
        self.level = LogLevelChoices.ERROR
        self.message = message
        self.save()
        return self

    def critical(self, message: str) -> Log:
        '''Insert a CRITICAL message.'''
        self.clear()
        self.level = LogLevelChoices.CRITICAL
        self.message = message
        self.save()
        return self

    def alert(self, message: str) -> Log:
        '''Insert an ALERT message.'''
        self.clear()
        self.level = LogLevelChoices.ALERT
        self.message = message
        self.save()
        return self

    def emergency(self, message: str) -> Log:
        '''Insert an EMERGENCY message.'''
        self.clear()
        self.level = LogLevelChoices.EMERGENCY
        self.message = message
        self.save()
        return self

    def exception(self, message: str) -> Log:
        '''Insert an EXCEPTION message.'''
        self.clear()
        self.level = LogLevelChoices.EXCEPTION
        self.message = message
        self.save()
        return self
