from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import UserLoginForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from pages.forms import RegisterForm

def index(request):
    return render(request,'pages/index.html')


def profile(request):
    return render(request,'pages/profile.html')

def login(request):
    
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user is not None:
                do_login(request, user)       
                return redirect('pages:index')

            else:
                messages.error(request,'username or password not correct')
                return redirect('pages:login')
    else:
        form = UserLoginForm()

    return render(request,'pages/login.html',{'form':form})
    

def logout(request):
    do_logout(request)
    return redirect('pages:login')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account succesfully created')
            return redirect('pages:login')
        else:
            messages.error(request,'An error ocurred')
    else:
        form = RegisterForm()
    return render(request,'pages/register.html',{'form':form})