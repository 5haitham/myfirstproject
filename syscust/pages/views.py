from django.shortcuts import render

from.models import login

# Create your views here.
def index(request):
    return render(request,'pages/index.html')


def about(request):

    username = request.POST.get('username')
    password=request.POST.get('password')

    data = login(username = username,password=password)
    data.save()
    return render(request,'pages/about.html')