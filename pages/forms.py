from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .utils import LANGUAGE_CHOICES
from .models import Profile


class ProfileEditForm(forms.ModelForm):
    first = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    speaks =  forms.MultipleChoiceField(choices = LANGUAGE_CHOICES, widget=forms.SelectMultiple(attrs={'class': 'form-control'})) 
    is_learning = forms.MultipleChoiceField(choices = LANGUAGE_CHOICES,widget=forms.SelectMultiple(attrs={'class': 'form-control'})) 
    class Meta:
        model = Profile
        fields = ['first','last','speaks','is_learning','photo']
        
    
    def from_value_to_label(self,method):
        list_label = [label for value, label in self.fields[method].choices if value in self[method].value()]
        print(self[method].value())
        # ['French', 'German']
        languages = ', '.join(list_label)
        # French, German
        return languages
    


        
       



class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username','password']


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(help_text='at least 8 characters',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    def clean_email(self):
            data = self.cleaned_data['email']
            if User.objects.filter(email=data).count() > 0:
                raise forms.ValidationError("We have a user with this user email-id")
            return data