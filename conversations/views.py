from django.shortcuts import redirect, render
from pages.models import Profile
from .forms import MessageForm
from .models import Chat,chat_members,Message
from django.utils import timezone

def inbox(request,profile_friend=None):
    
    profile = Profile.objects.get(id=request.user.profile.id)
    friends = profile.friends.all()
    

    if profile_friend is not None:
        p1 = Profile.objects.get(id=request.user.profile.id)
        p2 = Profile.objects.get(id=profile_friend)
        new_chat = Chat()
        new_chat.save()
        m1 = chat_members(chat=new_chat,profile=p1,deleted=False)
        m2 = chat_members(chat=new_chat,profile=p2,deleted=False)
        m1.save()
        m2.save()
        return redirect('conversations:inbox')
   
    
    chats_ids = profile.chats.all().values_list('chat_id', flat=True)
    chats = Chat.objects.filter(id__in = chats_ids)
 

    talking_with = []
    unread = []
    for c in chats:
        
        m_date = c.get_msg.values('date').latest('date')
        l_v = c.members.filter(profile = request.user.profile).values('last_viewed')
        if m_date['date'] > l_v[0]['last_viewed']:
            unread.append(True)
        else:
            unread.append(False) 
        chat_member = c.members.exclude(profile = request.user.profile)
        talking_with.append(chat_member)
        friends = friends.exclude(user = chat_member[0].profile.user)

    
    # print(talking_with[1][0].profile)
    # print(talking_with)
    

    

    context = {
    'profile':profile,
    'friends':friends,
    }
    context['chat_details'] = zip(talking_with, unread)
    
    return render(request,'conversations/inbox.html',context)


def chatbox(request,chat_id):
    
    profile = Profile.objects.get(id=request.user.profile.id)
    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_msg = form.save(commit=False)
            new_msg.profile = profile
            new_msg.chat = Chat.objects.get(id=chat_id)
            new_msg.save()
            return redirect('conversations:chatbox', chat_id=chat_id)
    
    messages = Message.objects.filter(chat_id=chat_id)

    last_viewed = chat_members.objects.filter(chat_id=chat_id).filter(profile=request.user.profile).values()
    last_viewed.update(last_viewed = timezone.now())


    context = {
        'chat_id':chat_id,
        'profile':profile,
        'form':form,
        'msg':messages,
        
    }

    return render(request,'conversations/chatbox.html',context)

