from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import UserLoginForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from pages.forms import RegisterForm,ProfileEditForm
from django.contrib.auth.models import User
from .models import FriendRequest,Profile
from django.db.models import Q

def index(request):
    
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        users = Profile.objects.exclude(user=request.user)
        
    else:
        users = Profile.objects.all
        profile = ''
        
    context = {
        'profile':profile,
        'users':users,
    }
    return render(request,'pages/index.html',context)


def profile(request,profile_id):
    
    profile = Profile.objects.get(id=profile_id)
    friends = profile.friends.all
    received_requests = FriendRequest.objects.filter(to_user=profile.user)
    
    button_text = ''
    if request.user.is_authenticated:
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


def from_label_to_value(request,field):
    LANGUAGE_CHOICES =( 
    ("1", "English"), 
    ("2", "Spanish"), 
    ("3", "French"), 
    ("4", "German"), 
    )
    if field == 'speaks':
        labels = request.user.profile.speaks
    else:
        labels = request.user.profile.is_learning

    if labels is not None:
        values = [value for value, label in LANGUAGE_CHOICES if label in labels]
        values = [int(i) for i in values]
    else:
        values = ''

    return values
    



def edit_profile(request):
    
    if request.method == 'POST':
        form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.speaks = form.selected_speaks_labels('speaks')
            obj.is_learning = form.selected_speaks_labels('is_learning')
            obj.save()
            
            
            return redirect('pages:profile', profile_id=request.user.profile.id)
    else:        
        
        
        is_learning = from_label_to_value(request, 'is_learning')
        speaks = from_label_to_value(request, 'speaks')
        
        
        form = ProfileEditForm(instance=request.user.profile,initial={'is_learning': is_learning, 'speaks':speaks })
        
        
    return render(request, 'pages/edit.html',{'form':form})


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



def search(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)  
    else:
        profile=''

    # english,''german','french'
    query = request.GET.get('q').replace(" ", "")
    # print(query)
    # get a list of values ['english','german','french']
    list_query = query.split(',')
    # print(list_query)
    results = Profile.objects.filter(speaks__icontains=list_query[0])

    if len(list_query)>1:
        for lq in range(len(list_query)-1):
            results = results.filter(speaks__icontains=list_query[lq+1])
    
    
    # print(results.values('speaks'))
    context = {
    'profile':profile,
    'users':results
    }

    return render(request,'pages/index.html',context)