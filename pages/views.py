from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import UserLoginForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from pages.forms import RegisterForm
from django.contrib.auth.models import User
from .models import FriendRequest,Profile

def index(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
    else:
        profiles = Profile.objects.all

    context = {
        'profiles':profiles
    }
    return render(request,'pages/index.html',context)


def profile(request,profile_id):
    profile = Profile.objects.get(id=profile_id)
    friends = profile.friends.all
    received_requests = FriendRequest.objects.filter(to_user=profile.user)
    
    button_text = ''
    if profile not in request.user.profile.friends.all():
        button_text = 'not_friend'
        if len(FriendRequest.objects.filter(from_user=request.user).filter(to_user=profile.user)) == 1:
	        button_text = 'request_sent'

    context = {
        'profile':profile,
        'id':profile.user.id,
        'friends':friends,
        'received_requests':received_requests,
        'button_text':button_text
    }
    return render(request,'pages/profile.html',context)


def send_request(request, to_user_id):
    if request.user.is_authenticated:
        to_user = User.objects.get(pk=to_user_id)
        frequest = FriendRequest.objects.get_or_create(
            from_user = request.user,
            to_user = to_user
        )
    return redirect('pages:profile', profile_id=to_user.profile.id)

def cancel_request(request,  to_user_id):
	if request.user.is_authenticated:
		to_user = User.objects.get(pk=to_user_id)
		frequest = FriendRequest.objects.filter(
			from_user=request.user,
			to_user=to_user).first()
		frequest.delete()
		return redirect('pages:profile',profile_id=to_user.profile.id)

def accept_friend_request(request, from_user_id):
	from_user = User.objects.get(id=from_user_id)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	user1 = frequest.to_user
	user2 = from_user
	user1.profile.friends.add(user2.profile)
	user2.profile.friends.add(user1.profile)
	frequest.delete()
	return redirect('pages:profile',profile_id=user1.profile.id)


def delete_friend_request(request, from_user_id):
	from_user = User.objects.get(id=from_user_id)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	frequest.delete()
	return redirect('pages:profile',profile_id=request.user.profile.id)

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