from django.db import models

class FixedCharField(models.Field):
    def __init__(self, max_length, *args, **kwargs):
        self.max_length = max_length
        super(FixedCharField, self).__init__(max_length=max_length, *args, **kwargs)

    def db_type(self, connection):
        return 'char(%s)' % (self.max_length,)
