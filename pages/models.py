from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    first = models.CharField(max_length=200,null=True,blank=True)
    last = models.CharField(max_length=200,null=True,blank=True)
    photo = models.ImageField(default='user.png',upload_to='photos/%Y/%m/',null=True,blank=True)

    def __str__(self):
        return str(self.user)



def create_profile(sender,instance,created, **kwargs):

    if created:
        Profile.objects.create(user=instance)
        print('profile')

post_save.connect(create_profile,sender=User)