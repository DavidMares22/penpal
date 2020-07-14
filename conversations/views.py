from django.shortcuts import redirect, render
from pages.models import Profile
from .models import Chat,chat_members

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

    chats = chat_members.objects.filter(profile = request.user.profile)
    print(chats)

    context = {
    'profile':profile,
    'friends':friends,
    'chats':chats,
    }
    
    return render(request,'conversations/inbox.html',context)


def chatbox(request):
    
    pass

    # return render(request,'conversations/chatbox.html')

