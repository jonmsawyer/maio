from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth import authenticate
from django.contrib.auth import login

from maio.forms import LoginForm


def home(request):
    cd = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username', '')
            password = form.cleaned_data.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = LoginForm()
    cd['form'] = form
    return render(request, 'maio/home.html', cd)
