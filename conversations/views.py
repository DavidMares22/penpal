from django.shortcuts import redirect, render
from pages.models import Profile
from .forms import MessageForm
from .models import Chat,chat_members,Message
from django.utils import timezone

def inbox(request,profile_friend=None):
    
    profile = Profile.objects.get(id=request.user.profile.id)
    friends = profile.friends.all()
    

    if profile_friend is not None:
        p2 = Profile.objects.get(id=profile_friend)
        chats_deleted = chat_members.objects.filter(profile_id = profile , deleted=True ).values_list('chat_id', flat=True)
        if chats_deleted:                        
            chat_with_friend = chat_members.objects.filter(chat_id__in = chats_deleted , profile_id=p2.id )
            if chat_with_friend:
                member = chat_members.objects.get(chat_id = chat_with_friend[0].chat_id , profile_id = request.user.profile.id)

                member.deleted = False
                member.save()

                return redirect('conversations:inbox')
        new_chat = Chat()
        new_chat.save()
        m1 = chat_members(chat=new_chat,profile=profile,deleted=False)
        m2 = chat_members(chat=new_chat,profile=p2,deleted=False)
        m1.save()
        m2.save()
        return redirect('conversations:inbox')
   
    
    chats_ids = profile.chats.all().values_list('chat_id', flat=True)
    chats = Chat.objects.filter(id__in = chats_ids)
 

    talking_with = []
    unread = []
    for c in chats:

        currrent_chat_member = c.members.get(profile = request.user.profile)
        if currrent_chat_member.deleted == False:
            chat_member = c.members.exclude(profile = request.user.profile)
            talking_with.append(chat_member)

        
            friends = friends.exclude(user = chat_member[0].profile.user)
            
            if c.get_msg.values('date').count() > 0:
                m_date = c.get_msg.values('date').latest('date')
                l_v = c.members.filter(profile = request.user.profile).values('last_viewed')
                if m_date['date'] > l_v[0]['last_viewed']:
                    unread.append(True)
                else:
                    unread.append(False)
            else:
                unread.append(False)

        

    
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


def delete_message(request,message_id):
    msg = Message.objects.get(id=message_id)
    msg.delete()
    return redirect('conversations:chatbox', chat_id=msg.chat_id )

def delete_chat(request,chat_id):
    member = chat_members.objects.get(chat_id = chat_id , profile_id = request.user.profile.id)

    member.deleted = True
    member.save()
    
     

    return redirect('conversations:inbox')

