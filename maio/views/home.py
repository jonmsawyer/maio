from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth import authenticate

from maio.models import ImageFile


def home(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            return redirect('dashboard')
    return render(request, 'maio/home.html', {})
