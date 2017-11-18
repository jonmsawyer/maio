from django.shortcuts import render

def home(request):
    cd ={}
    return render(request, 'maio/home.html', cd)
