from django.contrib.auth.views import PasswordChangeView as PCV
from django.contrib.auth.views import PasswordChangeDoneView as PCDV


class PasswordChangeView(PCV):
    '''Password Change View'''


class PasswordChangeDoneView(PCDV):
    '''Password Change Done View'''
