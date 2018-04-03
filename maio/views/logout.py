from django.shortcuts import redirect
from django.contrib.auth import logout as django_logout

def logout(request):
    django_logout(request)
    return redirect('home')
