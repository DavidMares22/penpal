from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    first = models.CharField(max_length=200,null=True,blank=True)
    last = models.CharField(max_length=200,null=True,blank=True)
    photo = models.ImageField(default='user.png',upload_to='photos/%Y/%m/',null=True,blank=True)
    friends = models.ManyToManyField('self',blank=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("pages:profile", kwargs={"profile_id": self.pk})
            



def create_profile(sender,instance,created, **kwargs):

    if created:
        Profile.objects.create(user=instance)
        print('profile')

post_save.connect(create_profile,sender=User)


class FriendRequest(models.Model):
    to_user = models.ForeignKey(User,related_name='to_user',on_delete=models.CASCADE)
    from_user = models.ForeignKey(User,related_name='from_user',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'From {self.from_user.username} to {self.to_user.username}'