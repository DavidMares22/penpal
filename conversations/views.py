from django.shortcuts import redirect, render
from pages.models import Profile
from .forms import MessageForm
from .models import Chat,chat_members,Message
from django.utils import timezone

def inbox(request,profile_friend=None):    
    profile = request.user.profile
    friends = profile.friends.all()
    
    if profile_friend is not None:
        p2 = friends.filter(id=profile_friend).first()
        chats_deleted = chat_members.objects.filter(profile = profile , deleted=True ).values_list('chat_id', flat=True)
        if chats_deleted:                        
            chat_with_friend = chat_members.objects.filter(chat_id__in = chats_deleted , profile_id=p2.id).first()
            if chat_with_friend:
                member = chat_members.objects.get(chat_id = chat_with_friend.chat_id , profile = profile)
                member.deleted = False
                member.save()
                return redirect('conversations:inbox')
        new_chat = Chat()
        new_chat.save()
        m1 = chat_members(chat=new_chat,profile=profile,deleted=False,last_viewed=timezone.now())
        m2 = chat_members(chat=new_chat,profile=p2,deleted=False, last_viewed=timezone.now())
        m1.save()
        m2.save()
        return redirect('conversations:inbox')
   
    
    chats_ids = profile.chats.all().values_list('chat_id', flat=True)
    chats = Chat.objects.filter(id__in = chats_ids)
    chatting_with = []
    unread = []

    for c in chats:
        profile_chat_member = c.members.get(profile = profile)
        if profile_chat_member.deleted == False:
            friend_chat_member = c.members.exclude(profile = profile).first()
            chatting_with.append(friend_chat_member)   
            friends = friends.exclude(user = friend_chat_member.profile.user)
            
            if c.get_msg.count() > 0:
                m_date = c.get_msg.values('date').latest('date')
                lv_date = c.members.filter(profile = profile).values('last_viewed').first()
            
                if m_date['date'] > lv_date['last_viewed']:
                    
                    msg_count = c.get_msg.filter(date__gt=lv_date['last_viewed']).count()
                    unread.append(msg_count)
                else:
                    unread.append(False)
            else:
                unread.append(False)


    context = {
    'profile':profile,
    'friends':friends,
    'chat_details': zip(chatting_with, unread)
    }
    return render(request,'conversations/inbox.html',context)


def chatbox(request,chat_id):   
    profile = request.user.profile
    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_msg = form.save(commit=False)
            new_msg.profile = profile
            new_msg.chat_id = chat_id
            new_msg.save()
            return redirect('conversations:chatbox', chat_id=chat_id)
    
    messages = Message.objects.filter(chat_id=chat_id)

    last_viewed = chat_members.objects.filter(chat_id=chat_id).filter(profile=profile)
    last_viewed.update(last_viewed = timezone.now())
    
    context = {
        'chat_id':chat_id,
        'profile':profile,
        'form':form,
        'msg':messages,
        
    }

    return render(request,'conversations/chatbox.html',context)


def delete_message(request,message_id):
    msg = Message.objects.get(id=message_id)
    msg.delete()
    return redirect('conversations:chatbox', chat_id=msg.chat_id )

def delete_chat(request,chat_id):
    chat = Chat.objects.get(id = chat_id)
    members = chat.members.all()
    for m in members:
        if m.profile == request.user.profile:
           profile = m
        else:
            friend = m

    if profile.deleted == False:
        profile.deleted = True
        profile.save()
    if friend.deleted == True:
        friend.delete() #we are usign signals as soon as delete member, chat gets deleted                  
    return redirect('conversations:inbox')

